from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Union, Dict, Any


def serialize_datetime(dt: Optional[datetime]) -> Optional[str]:
    return dt.isoformat() if dt else None


def deserialize_datetime(value: Optional[Union[str, datetime]]) -> Optional[datetime]:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value) if value else None


@dataclass
class GuidelineDownloadInformation:
    file_path: str = ""
    download_date: Optional[datetime] = None
    url: str = ""
    page_count: Optional[int] = None

    @staticmethod
    def from_dict(data: Dict):
        return GuidelineDownloadInformation(
            file_path=data.get("file_path", ""),
            download_date=deserialize_datetime(data.get("download_date")),
            url=data.get("url", ""),
            page_count=data.get("page_count")
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "download_date": serialize_datetime(self.download_date) if self.download_date else "",
            "url": self.url,
            "page_count": self.page_count
        }


@dataclass
class GuidelineValidityInformation:
    valid: bool = False
    extended_validity: bool = False
    guidelines_creation_date: Optional[datetime] = None

    @staticmethod
    def from_dict(data: Dict):
        return GuidelineValidityInformation(
            valid=data.get("valid", False),
            extended_validity=data.get("extended_validity", False),
            guidelines_creation_date=deserialize_datetime(data.get("guidelines_creation_date"))
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "extended_validity": self.extended_validity,
            "guidelines_creation_date": serialize_datetime(self.guidelines_creation_date) if self.guidelines_creation_date else "",
        }


@dataclass
class GuidelineMetadata:
    """Structured representation of a medical guideline entry."""
    awmf_register_number: str = ""
    awmf_class: str = ""
    title: str = ""
    leading_publishing_organizations: List[str] = field(default_factory=list)
    other_contributing_organizations: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    download_information: Optional[GuidelineDownloadInformation] = None
    validity_information: Optional[GuidelineValidityInformation] = None

    @staticmethod
    def from_dict(data: dict):
        return GuidelineMetadata(
            awmf_register_number=data.get("awmf_register_number", ""),
            awmf_class=data.get("awmf_class", ""),
            title=data.get("title", ""),
            leading_publishing_organizations=data.get("leading_publishing_organizations", []),
            other_contributing_organizations=data.get("other_contributing_organizations", []),
            keywords=data.get("keywords", []),
            download_information=GuidelineDownloadInformation.from_dict(data["download_information"]) if data.get("download_information") else None,
            validity_information=GuidelineValidityInformation.from_dict(data["validity_information"]) if data.get("validity_information") else None,
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "awmf_register_number": self.awmf_register_number,
            "awmf_class": self.awmf_class,
            "title": self.title,
            "leading_publishing_organizations": self.leading_publishing_organizations,
            "other_contributing_organizations": self.other_contributing_organizations,
            "keywords": self.keywords,
            "download_information": self.download_information.as_dict() if self.download_information else None,
            "validity_information": self.validity_information.as_dict() if self.validity_information else None,
        }
