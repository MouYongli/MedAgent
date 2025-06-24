from typing import Optional

import pandas as pd

from general.helper.logging import logger
from general.data_model.question_dataset import ExpectedAnswer
from general.helper.mongodb_interactor import CollectionName


def insert_question_classes(classes, question_types_collection):
    for qclass in classes:
        # Only insert if not already present
        qclass_dict = qclass.as_dict()
        if not question_types_collection.find_one(qclass_dict):
            question_types_collection.insert_one(qclass_dict)


def find_guideline(guideline_awmf_number: str, guideline_collection) -> Optional[dict]:
    if not guideline_awmf_number:
        return None

    guideline_query = {
        "awmf_register_number": {"$regex": guideline_awmf_number}
    }
    return guideline_collection.find_one(guideline_query)


def find_question_type(supercategory_str: str, subcategory_str: str, question_types_collection) -> Optional[dict]:
    query = {
        "supercategory": supercategory_str,
        "subcategory": subcategory_str
    }
    return question_types_collection.find_one(query)


def find_question(question_text: str, questions_collection) -> Optional[dict]:
    if not question_text:
        return None
    return questions_collection.find_one({"question": question_text})


def find_answer_for_question(question_doc: dict, answer_collection) -> Optional[list[dict]]:
    expected_answers = question_doc.get("expected_answers", [])
    if not expected_answers:
        return []
    return list(answer_collection.find({"_id": {"$in": expected_answers}}))


def insert_csv_entry_to_db(dbi, entry):
    """
    Inserts a single CSV-derived entry into MongoDB.
    - Overwrites answer for an existing question if needed.
    - Updates question metadata (e.g., classification) if inconsistent.
    """
    # --- Step 1: get all values, check if they are valid
    question_text = str(entry.get("Question")).strip()
    if not question_text:
        logger.error("Skipping entry: question is empty.")
        raise ValueError(f"Empty question")

    supercategory_str = str(entry.get("Question supercategory")).strip()
    subcategory_str = str(entry.get("Question subcategory")).strip()
    answer_text = str(entry.get("Answer")).strip() if pd.notna(entry.get("Answer")) else None
    guideline_awmf_number = str(entry.get("Answer Guideline")).strip() if pd.notna(entry.get("Answer Guideline")) else None
    raw_page = entry.get("Answer Gpage")
    guideline_page = int(str(raw_page).strip()) if (pd.notna(raw_page) and str(raw_page).strip().isdigit()) else None

    existing_class = find_question_type(supercategory_str, subcategory_str, dbi.get_collection(CollectionName.QUESTION_TYPES))
    if not existing_class:
        logger.error(
            f"Classification not found for question: '{question_text}' -> {supercategory_str}:{subcategory_str}")
        raise ValueError(f"Missing classification: {supercategory_str}:{subcategory_str}")
    question_class_id = existing_class["_id"]

    guideline_id = None
    if guideline_awmf_number:
        guideline = find_guideline(guideline_awmf_number, dbi.get_collection(CollectionName.GUIDELINES))
        if not guideline:
            logger.error(f"Guideline not found for answer in question: '{question_text}' -> {guideline_awmf_number}")
            raise ValueError(f"Missing guideline for answer: {guideline_awmf_number}")
        guideline_id = guideline["_id"]

    # --- STEP 2: Build the question --- #
    question = find_question(question_text, dbi.get_collection(CollectionName.QUESTIONS))
    if not question:
        new_question = {
            "question": question_text,
            "classification": question_class_id
        }
        dbi.get_collection(CollectionName.QUESTIONS).insert_one(new_question)
        logger.success(f"Inserted new question: '{question_text}'")
        question = find_question(question_text, dbi.get_collection(CollectionName.QUESTIONS))
    else:
        # Update classification if it differs
        if question.get("classification") != question_class_id:
            dbi.get_collection(CollectionName.QUESTIONS).update_one(
                {"_id": question["_id"]},
                {"$set": {"classification": question_class_id}}
            )
            logger.note(f"Classification updated for existing question: '{question_text}'")

    # --- STEP 3: Process answer ---
    if not answer_text:
        return  # No answer to process

    new_answer = ExpectedAnswer(text=answer_text, guideline_page=guideline_page)
    new_answer_dict = new_answer.as_dict()
    new_answer_dict["guideline"] = guideline_id

    # Check if an identical answer already exists
    existing_answers = find_answer_for_question(question, dbi.get_collection(CollectionName.CORRECT_ANSWERS))
    matched_answer = next((a for a in existing_answers if a["text"].strip() == answer_text.strip()), None)

    if matched_answer:
        # Update existing answer
        dbi.get_collection(CollectionName.CORRECT_ANSWERS).update_one(
            {"_id": matched_answer["_id"]},
            {"$set": new_answer_dict}
        )
        logger.note(f"Updated existing answer for question: '{question_text}'")
    else:
        # Insert new answer and attach to question
        new_expected_answer = dbi.get_collection(CollectionName.CORRECT_ANSWERS).insert_one(new_answer_dict).inserted_id
        dbi.get_collection(CollectionName.QUESTIONS).update_one(
            {"_id": question["_id"]},
            {"$push": {"expected_answers": new_expected_answer}}
        )
        logger.note(f"Added new answer to question: '{question_text}'")
