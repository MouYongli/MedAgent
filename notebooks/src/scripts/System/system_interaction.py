from typing import Optional, Tuple

import requests

from scripts.System.feedback_creation import create_feedback_response_latency
from general.data_model.question_dataset import QuestionEntry
from general.data_model.system_interactions import WorkflowSystem, ChatInteraction, GenerationResultEntry, Feedback, \
    FeedbackTarget, FeedbackType
from general.helper.logging import logger
from general.helper.mongodb_interactor import CollectionName, MongoDBInterface


def init_workflow(backend_api_url, config):
    response = requests.post(f"{backend_api_url}/workflow/init", json={"config": config})
    response.raise_for_status()
    workflow_id = response.json()["workflow_id"]
    return workflow_id

def init_workflow_with_id(backend_api_url, config, wf_id):
    response = requests.post(f"{backend_api_url}/workflow/init", json={"config": config, "workflow_id": wf_id})
    response.raise_for_status()
    workflow_id = response.json()["workflow_id"]
    return workflow_id  

def init_chat(backend_api_url, workflow_id):
    response = requests.post(f"{backend_api_url}/chat/init", json={"workflow_id": workflow_id})
    response.raise_for_status()
    chat_id = response.json()["chat_id"]
    return chat_id

def pose_question(backend_api_url, chat_id, question) -> Tuple[str, float]:
    response = requests.post(f"{backend_api_url}/chat/{chat_id}/ask", json={"question": question})
    response.raise_for_status()
    system_answer, response_latency = response.json()["response"], response.json()["response_latency"]
    return system_answer, response_latency

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

    generated_response, response_latency = pose_question(backend_api_url, chat.chat_id, question.question)
    entry = GenerationResultEntry.from_dict({
        "question": question.as_dict(),
        "answer": generated_response,
    })
    # collect first feedback
    entry.feedback.append(create_feedback_response_latency(response_latency))

    res = dbi.get_collection(CollectionName.GENERATION_RESULT_ENTRIES).insert_one({**entry.as_dict(), "question": question_doc["_id"]})

    dbi.get_collection(CollectionName.CHAT_INTERACTIONS).update_one(
        {"chat_id": chat.chat_id},
        {"$push": {"entries": res.inserted_id}},
    )
    return entry
