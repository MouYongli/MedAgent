import re
from typing import Optional, Tuple, Any, List

import requests

from scripts.System.feedback_creation import create_feedback_response_latency
from general.data_model.question_dataset import QuestionEntry, ExpectedAnswer
from general.data_model.system_interactions import WorkflowSystem, ChatInteraction, GenerationResultEntry, RetrievalEntry
from general.helper.logging import logger
from general.helper.mongodb_interactor import CollectionName, MongoDBInterface


def init_workflow(backend_api_url, config):
    # Get the list of all existing workflows
    response = requests.get(f"{backend_api_url}/workflow/list")
    response.raise_for_status()
    existing_workflows = response.json()

    # Check if any workflow exists already
    for workflow_id in existing_workflows:
        if existing_workflows[workflow_id] == "WorkflowSystem instance":
            logger.info(f"Workflow already exists with ID: {workflow_id}")
            return workflow_id  # Return the existing workflow ID

    # If no pre-existing system, initialize a new workflow
    response = requests.post(f"{backend_api_url}/workflow/init", json={"config": config})
    response.raise_for_status()
    workflow_id = response.json()["workflow_id"]
    return workflow_id


def init_workflow_with_id(backend_api_url, config, wf_id):
    # Check if the workflow with the given ID already exists
    response = requests.get(f"{backend_api_url}/workflow/{wf_id}")

    if response.status_code == 200:  # Workflow exists
        logger.info(f"Workflow with ID '{wf_id}' already exists.")
        return wf_id  # Return the existing workflow ID
    elif response.status_code != 404:  # Some other error occurred
        response.raise_for_status()

    # If the workflow doesn't exist, initialize it with the given ID
    response = requests.post(f"{backend_api_url}/workflow/init", json={"config": config, "workflow_id": wf_id})
    response.raise_for_status()
    workflow_id = response.json()["workflow_id"]
    return workflow_id

def init_chat(backend_api_url, workflow_id):
    response = requests.post(f"{backend_api_url}/chat/init", json={"workflow_id": workflow_id})
    response.raise_for_status()
    chat_id = response.json()["chat_id"]
    return chat_id

def pose_question(backend_api_url, chat_id, question) -> Tuple[str, Optional[Any], float]:
    response = requests.post(f"{backend_api_url}/chat/{chat_id}/ask", json={"question": question})
    response.raise_for_status()
    system_answer, retrieval_result, response_latency = response.json()["response"], response.json().get("retrieval", []), response.json()["response_latency"]
    return system_answer, retrieval_result, response_latency


def init_stored_wf_system(dbi: MongoDBInterface, config, backend_api_url) -> WorkflowSystem:
    wf_doc = dbi.get_entry(CollectionName.WORKFLOW_SYSTEMS, "name", config["name"])
    if wf_doc is None:
        wf_id = init_workflow(backend_api_url, config)
        wf_sys = WorkflowSystem.from_dict({
            "config": config,
            "name": config["name"],
            "workflow_id": wf_id
        })
        dbi.get_collection(CollectionName.WORKFLOW_SYSTEMS).insert_one(wf_sys.as_dict())
        return wf_sys
    else:
        # Ensure workflow exists in backend by re-initializing with same ID
        wf_id = init_workflow_with_id(backend_api_url, config, wf_doc["workflow_id"])
        return dbi.document_to_workflow_system(wf_doc)

def init_stored_chat(dbi: MongoDBInterface, wf_system: WorkflowSystem, backend_api_url) -> ChatInteraction:
    wf_doc = dbi.get_entry(CollectionName.WORKFLOW_SYSTEMS, "name", wf_system.name)
    if wf_doc is None:
        logger.error(f"Could not find workflow system {wf_system.name}")
        raise Exception(f"Could not find workflow system {wf_system.name}")

    chat_interaction  = ChatInteraction.from_dict({
        "chat_id": init_chat(backend_api_url, wf_system.workflow_id)
    })
    res = dbi.get_collection(CollectionName.CHAT_INTERACTIONS).insert_one(chat_interaction.as_dict())
    dbi.get_collection(CollectionName.WORKFLOW_SYSTEMS).update_one(
        {"name": wf_system.name},
        {"$push": {"generation_results": res.inserted_id}},
    )
    return chat_interaction

def create_retrieval_scores(
        expected_retrieval: List[ExpectedAnswer],
        actual_retrieval: List[RetrievalEntry]
):
    logger.info("Starting retrieval evaluation...")
    logger.info(f"Number of expected entries: {len(expected_retrieval)}")
    logger.info(f"Number of actual entries: {len(actual_retrieval)}")

    # TODO: count True positives etc.
    def normalize(text: str) -> str:
        norm = re.sub(r'[\s\-•]+', '', text).lower()
        logger.debug(f"Normalized text: '{text}' -> '{norm}'")
        return norm

    def longest_common_substring(s1: str, s2: str) -> str:
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_len = 0
        end_pos_s1 = 0

        for i in range(m):
            for j in range(n):
                if s1[i] == s2[j]:
                    dp[i + 1][j + 1] = dp[i][j] + 1
                    if dp[i + 1][j + 1] > max_len:
                        max_len = dp[i + 1][j + 1]
                        end_pos_s1 = i + 1

        lcs = s1[end_pos_s1 - max_len:end_pos_s1]
        logger.debug(f"Longest substring between \n{s1} \nand \n{s2}\n:\n{lcs}")
        return lcs

    def find_and_remove_substring(substring: str, s1: str, s2: str) -> Tuple[bool, str, str]:
        if (s1.find(substring) == -1) or (s2.find(substring) == -1):
            logger.debug(f"Substring {substring} not found in \n{s1} \nor \n{s2}")
            return False, s1, s2
        else:
            logger.debug(f"Found substring {substring} in \n{s1} \nand \n{s2}\n--> removing")
            s1 = s1.replace(substring, '')
            s2 = s2.replace(substring, '')
            logger.debug(f"Result after removing:\n{s1} \nand \n{s2}")
            return True, s1, s2

    normalized_expected_retrieval, normalized_actual_retrieval = expected_retrieval.copy(), actual_retrieval.copy()
    for er in normalized_expected_retrieval:
        er.text = normalize(er.text)
    for ar in normalized_actual_retrieval:
        ar.text = normalize(ar.text)

    original_lengths_expected_retrieval, original_lengths_actual_retrieval = [len(er.text) for er in normalized_expected_retrieval], [len(ar.text) for ar in normalized_actual_retrieval]
    partial_tp_expected_retrieval, partial_fn_expected_retrieval = [0] * len(normalized_expected_retrieval), [0] * len(normalized_expected_retrieval)
    partial_tp_actual_retrieval, partial_fp_actual_retrieval = [0] * len(normalized_actual_retrieval), [0] * len(normalized_actual_retrieval)

    substrings = []
    for i_er, er in enumerate(normalized_expected_retrieval):
        for i_ar, ar in enumerate(normalized_actual_retrieval):
            lcs = longest_common_substring(er.text, ar.text)
            if len(lcs) > 0:
                substrings.append({
                    "lcs": lcs,
                    "er_index": i_er,
                    "ar_index": i_ar
                })

    for substring in sorted(substrings, key=lambda x: len(x['lcs']), reverse=True):
        logger.info(f"For substring: {substring['lcs']} of length {len(substring['lcs'])}")
        found, normalized_expected_retrieval[substring['er_index']].text, normalized_actual_retrieval[substring['ar_index']].text = find_and_remove_substring(substring['lcs'], normalized_expected_retrieval[substring['er_index']].text, normalized_actual_retrieval[substring['ar_index']].text)
        if found:
            partial_tp_expected = len(substring['lcs']) / original_lengths_expected_retrieval[substring['er_index']]
            partial_tp_actual = len(substring['lcs']) / original_lengths_actual_retrieval[substring['ar_index']]

            partial_tp_expected_retrieval[substring['er_index']] += partial_tp_expected
            partial_tp_actual_retrieval[substring['ar_index']] += partial_tp_actual

            logger.info(f"Partial TP for expected: {len(substring['lcs'])} / {original_lengths_expected_retrieval[substring['er_index']]} = {partial_tp_expected}\n --> Now at value {partial_tp_expected_retrieval[substring['er_index']]} for the expected entry")
            logger.info(f"Partial TP for retrieved: {len(substring['lcs'])} / {original_lengths_actual_retrieval[substring['ar_index']]} = {partial_tp_actual}\n --> Now at value {partial_tp_actual_retrieval[substring['ar_index']]} for the retrieved entry")
        else:
            logger.info(f"Skipped")

    for i_er, er in enumerate(normalized_expected_retrieval):
        if len(er.text) > 0:
            partial_fn_expected_retrieval[i_er] = len(er.text) / original_lengths_expected_retrieval[i_er]
            logger.info(f"[Expected {i_er}]  partial TP: {partial_tp_expected_retrieval[i_er]:.2f}; partial FN {partial_fn_expected_retrieval[i_er]:.2f} (should be {(1-partial_tp_expected_retrieval[i_er]):.2f})")
    for i_ar, ar in enumerate(normalized_actual_retrieval):
        if len(ar.text) > 0:
            partial_fp_actual_retrieval[i_ar] = len(ar.text) / original_lengths_actual_retrieval[i_ar]
            logger.info(f"[Actual   {i_ar}]  partial TP: {partial_tp_actual_retrieval[i_ar]:.2f}; partial FP {partial_fp_actual_retrieval[i_ar]:.2f} (should be {(1-partial_tp_actual_retrieval[i_ar]):.2f})")

    tp_retrieval = sum(partial_tp_actual_retrieval)
    tp_expectation = sum(partial_tp_expected_retrieval)
    fp = sum(partial_fp_actual_retrieval)
    fn = sum(partial_fn_expected_retrieval)

    precision = tp_retrieval / (tp_retrieval + fp)
    recall = tp_expectation / (tp_expectation + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    logger.info(
        f"""Summed results:
        [Expected ] TP: {(sum(partial_tp_expected_retrieval)):.2f}, FN: {(sum(partial_fn_expected_retrieval)):.2f}, max possible: {len(partial_tp_expected_retrieval)}
        [Actual   ] TP: {(sum(partial_tp_actual_retrieval)):.2f}, FP: {(sum(partial_fp_actual_retrieval)):.2f}, max possible: {len(partial_tp_actual_retrieval)}
        [Return   ] Precision: {precision}, Recall: {recall}, F1: {f1}
        """
    )
    return precision, recall, f1

def generate_stored_response(
        dbi: MongoDBInterface, wf_system: WorkflowSystem, chat: Optional[ChatInteraction], question: QuestionEntry, backend_api_url
) -> GenerationResultEntry:
    if chat is None:
        chat = init_stored_chat(dbi, wf_system, backend_api_url)
    if dbi.get_entry(CollectionName.CHAT_INTERACTIONS, "chat_id", chat.chat_id) is None:
        logger.error(f"Could not find chat {chat.chat_id}")
        raise Exception(f"Could not find chat {chat.chat_id}")

    question_doc = dbi.get_entry(CollectionName.QUESTIONS, "question", question.question)
    if question_doc is None:
        logger.error(f"Could not find question {question.question}")
        raise Exception(f"Could not find question {question.question}")

    generated_response, retrieval, response_latency = pose_question(backend_api_url, chat.chat_id, question.question)
    entry = GenerationResultEntry.from_dict({
        "question": question.as_dict(),
        "answer": generated_response,
    })
    for retrieval_entry in retrieval:
        gl = dbi.document_to_guideline_metadata(dbi.get_entry(CollectionName.GUIDELINES, "awmf_register_number", retrieval_entry["guideline_id"]))
        entry.retrieval_result.append(
            RetrievalEntry(
                text=retrieval_entry["text"],
                guideline=gl
            )
        )
    # collect first feedback
    entry.feedback.append(create_feedback_response_latency(response_latency))
    retrieval_precision, retrieval_recall, retrieval_f1 = create_retrieval_scores(entry.question.expected_answers, entry.retrieval_result)

    res = dbi.get_collection(CollectionName.GENERATION_RESULT_ENTRIES).insert_one(
        {**entry.as_dict(), "question": question_doc["_id"]}
    )

    dbi.get_collection(CollectionName.CHAT_INTERACTIONS).update_one(
        {"chat_id": chat.chat_id},
        {"$push": {"entries": res.inserted_id}},
    )
    return entry
