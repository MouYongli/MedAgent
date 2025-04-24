# general/helper/mongodb_interactor.py

from enum import Enum
from typing import Dict, Any

from bson import ObjectId
from pymongo import MongoClient

from general.data_model.guideline_metadata import GuidelineMetadata
from general.data_model.question_dataset import QuestionEntry, QuestionClass, ExpectedAnswer
from general.data_model.system_interactions import RetrievalEntry
from general.data_model.system_interactions import WorkflowSystem, GenerationResultEntry, ChatInteraction
from general.helper.logging import logger


class CollectionName(str, Enum):
    GUIDELINES = "guidelines"
    QUESTIONS = "questions"
    QUESTION_TYPES = "question_types"
    CORRECT_ANSWERS = "expected_answers"
    WORKFLOW_SYSTEMS = "workflow_systems"
    CHAT_INTERACTIONS = "chats"
    GENERATION_RESULT_ENTRIES = "generation_result_entries"
    # Add more as needed


class MongoDBInterface:
    def __init__(self, uri: str, db_name: str = "nb_document_store"):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self.db = self.client[db_name]
        self.collections = {}

    def register_collections(self, *collection_names: CollectionName):
        """
        Registers multiple collections for easy access later via self.collections.
        """
        for name in collection_names:
            self.collections[name] = self.db[name.value]

    def get_collection(self, name: CollectionName):
        return self.collections.get(name, self.db[name.value])

    def get_entry(self, collection_name: CollectionName, key_name: str, key_value):
        """
        Retrieve a document by its _id from the given collection.

        Returns None if not found or if object_id is invalid.
        """
        try:
            return self.get_collection(collection_name).find_one({key_name: key_value})
        except Exception:
            return None

    def document_to_question_class(self, doc: Dict) -> QuestionClass:
        return QuestionClass.from_dict(doc)

    def document_to_answer(self, doc: Dict) -> ExpectedAnswer:
        answer = ExpectedAnswer.from_dict({k: v for k, v in doc.items() if k not in {"guideline"}})

        guideline_doc = self.get_entry(CollectionName.GUIDELINES, "_id", ObjectId(doc["guideline"]))
        if guideline_doc:
            answer.guideline = self.document_to_guideline_metadata(guideline_doc)
        else:
            logger.error(f"Failed to load GuidelineMetadata with ID: {doc['guideline']}")
            raise ValueError(f"Missing GuidelineMetadata: {doc['guideline']}")

        return answer

    def document_to_question_entry(self, question_doc: Dict) -> QuestionEntry:
        """
        Fully hydrate a QuestionEntry from its DB document.
        Resolves:
          - classification (via QUESTION_TYPES collection)
          - answers (via CORRECT_ANSWERS collection)
        """
        entry = QuestionEntry.from_dict(
            {k: v for k, v in question_doc.items() if k not in {"classification", "expected_answers"}})

        # Resolve classification
        if ("classification" in question_doc) and question_doc["classification"]:
            class_doc = self.get_entry(CollectionName.QUESTION_TYPES, "_id", ObjectId(question_doc["classification"]))
            if class_doc:
                entry.classification = self.document_to_question_class(class_doc)
            else:
                logger.error(f"Failed to load QuestionClass with ID: {question_doc['classification']}")
                raise ValueError(f"Missing QuestionClass: {question_doc['classification']}")

        # Resolve answers
        entry.expected_answers = []
        for answer_id in question_doc.get("expected_answers", []):
            answer_doc = self.get_entry(CollectionName.CORRECT_ANSWERS, "_id", ObjectId(answer_id))
            if answer_doc:
                entry.expected_answers.append(self.document_to_answer(answer_doc))
            else:
                logger.error(f"Failed to load Answer with ID: {answer_id}")
                raise ValueError(f"Missing Answer: {answer_id}")

        return entry

    def document_to_generation_result_entry(self, doc: Dict[str, Any]) -> GenerationResultEntry:
        gen_res = GenerationResultEntry.from_dict(
            {k: v for k, v in doc.items() if k not in {"question", "retrieval_result"}})

        # Resolve QuestionEntry
        question_doc = self.get_entry(CollectionName.QUESTIONS, "_id", doc["question"])
        if question_doc:
            gen_res.question = self.document_to_question_entry(question_doc)
        else:
            logger.error(f"Failed to load QuestionEntry with ID: {doc['question']}")
            raise ValueError(f"Missing QuestionEntry: {doc['question']}")

        # Resolve RetrievalResults
        for rr in doc.get("retrieval_result", []):
            gl_object_id = rr.get("guideline")
            if gl_object_id:
                gl_doc = self.get_entry(CollectionName.GUIDELINES, "_id", gl_object_id)
                if gl_doc:
                    gl = self.document_to_guideline_metadata(gl_doc)
                    rr_obj = RetrievalEntry(text=rr.get("text"), guideline=gl)
                    gen_res.retrieval_result.append(rr_obj)
                else:
                    logger.error(f"Failed to load GuidelineMetadata with ObjectId: {gl_object_id}")
                    raise ValueError(f"Missing GuidelineMetadata: {gl_object_id}")
            else:
                logger.error(f"RetrievalResult entry missing guideline: {rr}")

        return gen_res

    def document_to_chat_interaction(self, chat_doc: Dict[str, Any]) -> ChatInteraction:
        """
        Fully hydrate a ChatInteraction from its DB document.
        Resolves:
          - entries (via GENERATION_RESULT_ENTRIES collection)
        """
        chat = ChatInteraction.from_dict({k: v for k, v in chat_doc.items() if k not in {"entries"}})

        chat.entries = []
        for entry_id in chat_doc.get("entries", []):
            entry_doc = self.get_entry(CollectionName.GENERATION_RESULT_ENTRIES, "_id", entry_id)
            if entry_doc:
                chat.entries.append(self.document_to_generation_result_entry(dict(entry_doc)))
            else:
                logger.error(f"Failed to load GenerationResultEntry with ID: {entry_id}")
                raise ValueError(f"Missing GenerationResultEntry: {entry_id}")
        return chat

    def document_to_workflow_system(self, wf_doc: Dict[str, Any]) -> WorkflowSystem:
        """
        Fully hydrate a WorkflowSystem from its DB document.
        Resolves:
          - generation_results (via GENERATION_RESULTS collection)
        """
        wf = WorkflowSystem.from_dict({k: v for k, v in wf_doc.items() if k not in {"generation_results"}})

        wf.generation_results = []
        for chat_id in wf_doc.get("generation_results", []):
            chat_doc = self.get_entry(CollectionName.CHAT_INTERACTIONS, "_id", chat_id)
            if chat_doc:
                wf.generation_results.append(self.document_to_chat_interaction(dict(chat_doc)))
            else:
                logger.error(f"Failed to load ChatInteraction with chat_id: {chat_id}")
                raise ValueError(f"Missing ChatInteraction: {chat_id}")

        return wf

    def document_to_guideline_metadata(self, doc: dict) -> GuidelineMetadata:
        return GuidelineMetadata.from_dict(doc)

    def close(self):
        self.client.close()
