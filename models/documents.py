from datetime import date
from typing import Optional

from .users import User, find_user_by_id


class Document:
    """Документ с ограниченным сроком действия."""

    def __init__(self, doc_id: int, title: str, number: str,
                 expiry: date, owner: User) -> None:
        self.id = doc_id
        self.title = title
        self.number = number
        self.expiry = expiry
        self.owner = owner

    def __str__(self) -> str:
        days_left = self.days_until_expiry(date.today())
        return (f"[{self.id}] {self.title} ({self.number}) — "
                f"до {self.expiry.isoformat()} — {self.get_status(days_left)}")

    def days_until_expiry(self, current: date) -> int:
        return (self.expiry - current).days

    def get_status(self, days_left: int) -> str:
        if days_left < 0:
            return "ПРОСРОЧЕН"
        elif days_left == 0:
            return "ИСТЕКАЕТ СЕГОДНЯ"
        elif days_left <= 30:
            return "ИСТЕКАЕТ СКОРО"
        else:
            return "ДЕЙСТВИТЕЛЕН"

    def format_notification(self, days_left: int) -> str:
        if days_left < 0:
            return (f"{self.owner.name}, документ «{self.title}» "
                    f"просрочен на {abs(days_left)} дн.")
        return (f"{self.owner.name}, до окончания «{self.title}» "
                f"осталось {days_left} дн.")

    @classmethod
    def from_data(cls, data: dict, users: list[User]) -> Optional["Document"]:
        owner = find_user_by_id(users, data["owner_id"])
        if owner is None:
            return None
        return cls(
            doc_id=data["id"],
            title=data["title"],
            number=data["number"],
            expiry=date.fromisoformat(data["expiry"]),
            owner=owner,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "number": self.number,
            "expiry": self.expiry.isoformat(),
            "owner_id": self.owner.id,
        }


def add_document(documents: list[Document], title: str, number: str,
                 expiry: date, owner: User) -> Document:
    doc_id = len(documents) + 1
    doc = Document(doc_id, title, number, expiry, owner)
    documents.append(doc)
    return doc


def find_documents(documents: list[Document], query: str) -> list[Document]:
    result = []
    for doc in documents:
        if query.lower() in doc.title.lower():
            result.append(doc)
    return result


def find_document_by_id(documents: list[Document],
                        doc_id: int) -> Optional[Document]:
    for doc in documents:
        if doc.id == doc_id:
            return doc
    return None


def get_expiring_documents(documents: list[Document],
                           threshold: int = 30) -> list[Document]:
    today = date.today()
    result = []
    for doc in documents:
        if doc.days_until_expiry(today) <= threshold:
            result.append(doc)
    return result


def sort_documents_by_expiry(documents: list[Document]) -> list[Document]:
    return sorted(documents, key=lambda d: d.expiry)


def get_statistics(documents: list[Document]) -> dict:
    today = date.today()
    stats = {"total": len(documents), "expired": 0,
             "expiring": 0, "valid": 0}
    for doc in documents:
        days_left = doc.days_until_expiry(today)
        if days_left < 0:
            stats["expired"] += 1
        elif days_left <= 30:
            stats["expiring"] += 1
        else:
            stats["valid"] += 1
    return stats


def show_documents(documents: list[Document]) -> None:
    if not documents:
        print("Список документов пуст.")
        return
    for doc in documents:
        print(doc)
