from datetime import date
from typing import Optional

from .users import User, find_user_by_id
from .documents import Document, find_document_by_id


class Notification:

    def __init__(self, note_id: int, user: User,
                 document: Document, message: str) -> None:
        self.id = note_id
        self.user = user
        self.document = document
        self.message = message
        self.created = date.today()

    def __str__(self) -> str:
        return (f"[{self.id}] {self.created.isoformat()} — "
                f"{self.user.name}: {self.message}")

    @classmethod
    def from_data(cls, data: dict, users: list[User],
                  documents: list[Document]) -> Optional["Notification"]:
        user = find_user_by_id(users, data["user_id"])
        document = find_document_by_id(documents, data["document_id"])
        if user is None or document is None:
            return None
        note = cls(
            note_id=data["id"],
            user=user,
            document=document,
            message=data["message"],
        )
        note.created = date.fromisoformat(data["created"])
        return note

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user.id,
            "document_id": self.document.id,
            "message": self.message,
            "created": self.created.isoformat(),
        }


def create_notification(user: User, document: Document,
                        message: str) -> Notification:
    return Notification(0, user, document, message)


def add_notification(notifications: list[Notification],
                     notification: Notification) -> Notification:
    notification.id = len(notifications) + 1
    notifications.append(notification)
    return notification


def show_notifications(notifications: list[Notification]) -> None:
    if not notifications:
        print("Список уведомлений пуст.")
        return
    for note in notifications:
        print(note)
