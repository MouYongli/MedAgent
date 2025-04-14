from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Union, Optional, Literal
from uuid import UUID

from general.data_model.guideline_metadata import serialize_datetime, deserialize_datetime
from general.data_model.question_dataset import QuestionEntry, SuperCategory, SubCategory


@dataclass
class WorkflowSystem:
    name: str
    workflow_id: UUID
    config: Dict  # JSON-like structure
    generation_results: List["ChatInteraction"] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "WorkflowSystem":
        return WorkflowSystem(
            workflow_id=data.get("workflow_id"),
            name=data.get("name"),
            config=data["config"],
            generation_results=data.get("generation_results", [])
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "workflow_id": self.workflow_id,
            "config": self.config,
            "generation_results": [
                gen_res.as_dict() for gen_res in self.generation_results
            ],
        }

    def get_all_questions_for_super_category(self, super_cat: SuperCategory) -> List["GenerationResultEntry"]:
        res = []
        for chat in self.generation_results:
            for gen_res in chat.entries:
                if gen_res.question.classification.supercategory == super_cat:
                    res.append(gen_res)
        return res

    def get_all_questions_for_sub_category(self, super_cat: SuperCategory, sub_cat: SubCategory) -> List["GenerationResultEntry"]:
        res = []
        for chat in self.generation_results:
            for gen_res in chat.entries:
                classification = gen_res.question.classification
                if (classification.supercategory == super_cat) and (classification.subcategory == sub_cat):
                    res.append(gen_res)
        return res

@dataclass
class ChatInteraction:
    chat_id: UUID
    entries: List["GenerationResultEntry"] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ChatInteraction":
        return ChatInteraction(
            chat_id=data["chat_id"],
            entries=data.get("entries", [])
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "chat_id": self.chat_id,
            "entries": [
                entry.as_dict() for entry in self.entries
            ]
        }


@dataclass
class GenerationResultEntry:
    question: Optional[QuestionEntry]
    answer: str
    feedback: List["Feedback"] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GenerationResultEntry":
        return GenerationResultEntry(
            question=QuestionEntry.from_dict(data["question"]) if data.get("question") else None,
            answer=data["answer"],
            feedback=[
                Feedback.from_dict(fb) for fb in data.get("feedback", [])
            ]
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question.as_dict(),
            "answer": self.answer,
            "feedback": [
                fb.as_dict() for fb in self.feedback
            ]
        }

    def get_response_latency(self) -> Optional[float]:
        for feedback in self.feedback:
            if feedback.type == FeedbackType.RESPONSE_LATENCY:
                return feedback.value
        return None

    def get_correctness_score(self) -> Optional["correctness_likert"]:
        for feedback in self.feedback:
            if feedback.type == FeedbackType.CORRECTNESS:
                return feedback.value
        return None

    def get_hallucination_classification(self) -> Optional[Dict[str, int]]:
        for feedback in self.feedback:
            if feedback.type == FeedbackType.HALLUCINATION:
                return feedback.value
        return None

class FeedbackTarget(Enum):
    SYSTEM = "System"
    RETRIEVER = "Retriever"
    GENERATOR = "Generator"
    RETRIEVAL_SOURCE = "RetrievalSource"


class FeedbackType(Enum):
    CORRECTNESS = "Correctness"
    HALLUCINATION = "Hallucination classification"
    RESPONSE_LATENCY = "Response latency"
    RETRIEVAL_RECALL = "Retrieval Recall"
    RETRIEVAL_PRECISION = "Retrieval Precision"
    RETRIEVAL_F1 = "Retrieval F1"
    FACTUALITY = "Factuality Score"
    CREATION_TIME = "Full creation time"
    UPDATE_TIME = "Update time"

correctness_likert = Literal[1, 2, 3, 4, 5]

@dataclass
class Feedback:
    target: FeedbackTarget
    type: FeedbackType
    value: Union[int, float, str, Dict[str, int], correctness_likert]  # e.g., Likert scale, ratio, category counts
    manual: bool = False
    notes: Optional[str] = None
    timestamp: Optional[datetime] = field(default_factory=datetime.utcnow)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Feedback":
        return Feedback(
            target=FeedbackTarget(data["target"]),
            type=FeedbackType(data["type"]),
            value=data["value"],
            manual=data.get("manual", False),
            notes=data.get("notes"),
            timestamp=deserialize_datetime(data["timestamp"]) if data.get("timestamp") else None
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "target": self.target.value,
            "type": self.type.value,
            "value": self.value,
            "manual": self.manual,
            "notes": self.notes,
            "timestamp": serialize_datetime(self.timestamp)
        }

