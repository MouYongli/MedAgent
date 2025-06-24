from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union, Dict, Any

from general.data_model.guideline_metadata import GuidelineMetadata


class SuperCategory(Enum):
    SIMPLE = "Simple"
    COMPLEX = "Complex"
    NEGATIVE = "Negative"


class SimpleSubCategory(Enum):
    TEXT = "Text"
    TABLE = "Table"
    IMAGE = "Image"
    RECOMMENDATION = "Recommendation"


class ComplexSubCategory(Enum):
    SYNONYM = "Synonym"
    MULTIPLE_SECTIONS = "Multiple sections"
    MULTIPLE_GUIDELINES = "Multiple guidelines"
    SUBSTEPS = "Substeps"


class NegativeSubCategory(Enum):
    OUTSIDE_MEDICINE = "Outside medicine"
    OUTSIDE_OMS = "Outside OMS"
    OUTSIDE_GUIDELINES = "Outside guidelines"
    PATIENT_SPECIFIC = "Patient-specific"
    BROKEN_INPUT = "Broken input"
    FALSE_ASSUMPTION = "False assumption"

SubCategory = Union[SimpleSubCategory, ComplexSubCategory, NegativeSubCategory]

@dataclass(frozen=True)
class QuestionClass:
    supercategory: SuperCategory
    subcategory: SubCategory

    @staticmethod
    def from_dict(data: Dict[str, str]) -> "QuestionClass":
        sup = SuperCategory(data["supercategory"])
        sub_enum_map = {
            SuperCategory.SIMPLE: SimpleSubCategory,
            SuperCategory.COMPLEX: ComplexSubCategory,
            SuperCategory.NEGATIVE: NegativeSubCategory,
        }
        sub = sub_enum_map[sup](data["subcategory"])
        return QuestionClass(supercategory=sup, subcategory=sub)

    def as_dict(self) -> Dict[str, str]:
        return {
            "supercategory": self.supercategory.value,
            "subcategory": self.subcategory.value
        }

all_question_classes = [
    QuestionClass(supercat, subcat)
    for supercat, sub_enum in {
        SuperCategory.SIMPLE: SimpleSubCategory,
        SuperCategory.COMPLEX: ComplexSubCategory,
        SuperCategory.NEGATIVE: NegativeSubCategory
    }.items()
    for subcat in sub_enum
]

all_supercategories = [
    SuperCategory.SIMPLE,
    SuperCategory.COMPLEX,
    SuperCategory.NEGATIVE
]


@dataclass
class ExpectedAnswer:
    text: str
    guideline: Optional[GuidelineMetadata] = None
    guideline_page: Optional[int] = None

    @staticmethod
    def from_dict(data: Dict) -> "ExpectedAnswer":
        return ExpectedAnswer(
            text=data.get("text", ""),
            guideline=GuidelineMetadata.from_dict(data["guideline"]) if data.get("guideline") else None,
            guideline_page=data.get("guideline_page")
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "guideline": self.guideline.as_dict() if self.guideline else None,
            "guideline_page": self.guideline_page
        }


@dataclass
class QuestionEntry:
    question: str
    classification: Optional[QuestionClass] = None
    expected_answers: List[ExpectedAnswer] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict) -> "QuestionEntry":
        return QuestionEntry(
            question=data.get("question", ""),
            classification=QuestionClass.from_dict(data["classification"]) if data.get("classification") else None,
            expected_answers=[ExpectedAnswer.from_dict(a) for a in data.get("expected_answers", [])],
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "classification": self.classification.as_dict() if self.classification else None,
            "expected_answers": [
                answer.as_dict() for answer in self.expected_answers
            ]
        }
