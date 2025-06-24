from typing import Optional, Dict

from general.data_model.system_interactions import Feedback, FeedbackTarget, FeedbackType, ChatInteraction, GenerationResultEntry
from general.helper.logging import logger
from general.helper.mongodb_interactor import MongoDBInterface, CollectionName


def create_feedback_response_latency(response_latency: float) -> Feedback:
    response_latency_feedback = Feedback(
        target=FeedbackTarget.SYSTEM,
        type=FeedbackType.RESPONSE_LATENCY,
        value=response_latency,
    )
    return response_latency_feedback

def create_feedback_correctness(score: int, notes: Optional[str] = None) -> Feedback:
    return Feedback(
        target=FeedbackTarget.SYSTEM,
        type=FeedbackType.CORRECTNESS,
        value=score,
        manual=True,
        notes=notes
    )

def create_feedback_hallucination_classification(counts: Dict[str, int], notes: Optional[str] = None) -> Feedback:
    return Feedback(
        target=FeedbackTarget.SYSTEM,
        type=FeedbackType.HALLUCINATION,
        value=counts,  # e.g., {"FC": 1, "IC": 0, "CC": 2}
        manual=True,
        notes=notes
    )

def insert_feedback(dbi: MongoDBInterface, chat: ChatInteraction, entry: GenerationResultEntry, feedback: Feedback):
    chat_doc = dbi.get_entry(CollectionName.CHAT_INTERACTIONS, "chat_id", chat.chat_id)
    if chat_doc is None:
        logger.error(f"Could not find chat {chat.chat_id}")
        raise Exception(f"Could not find chat {chat.chat_id}")

    possible_entry_ids = chat_doc.get("entries", [])
    question_id = dbi.get_entry(CollectionName.QUESTIONS, "question", entry.question.question).get("_id")

    matching_entry = dbi.get_collection(CollectionName.GENERATION_RESULT_ENTRIES).find_one({
        "question": question_id,
        "answer": entry.answer,
        "_id": {"$in": possible_entry_ids}
    })
    if matching_entry is None:
        logger.error("No matching GenerationResultEntry found to attach feedback.")
        raise Exception("Feedback insertion failed: no matching GenerationResultEntry.")

    print(matching_entry)

    result = dbi.get_collection(CollectionName.GENERATION_RESULT_ENTRIES).update_one(
        {"_id": matching_entry["_id"]},
        {"$push": {"feedback": feedback.as_dict()}}
    )

    if result.modified_count == 0:
        logger.error(f"Feedback push failed for entry {matching_entry['_id']}")
        raise Exception("Feedback insertion failed: update operation did not modify entry.")
    else:
        logger.info(f"Feedback inserted for entry {matching_entry['_id']} in chat {chat.chat_id}.")



