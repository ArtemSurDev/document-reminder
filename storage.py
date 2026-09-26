import json
import os

from models import User, Document, Notification


DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.json")
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, "notifications.json")


def _load_raw(filename: str) -> list[dict]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, начинаем с пустого списка.")
        return []


def _save_raw(filename: str, data: list[dict]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_users(filename: str = USERS_FILE) -> list[User]:
    raw = _load_raw(filename)
    return [User.from_data(item) for item in raw]


def save_users(users: list[User], filename: str = USERS_FILE) -> None:
    _save_raw(filename, [user.to_dict() for user in users])


def load_documents(filename: str = DOCUMENTS_FILE,
                   users: list[User] | None = None) -> list[Document]:
    raw = _load_raw(filename)
    if users is None:
        users = load_users()
    documents = []
    for item in raw:
        doc = Document.from_data(item, users)
        if doc is not None:
            documents.append(doc)
    return documents


def save_documents(documents: list[Document],
                   filename: str = DOCUMENTS_FILE) -> None:
    _save_raw(filename, [doc.to_dict() for doc in documents])


def load_notifications(filename: str = NOTIFICATIONS_FILE,
                       users: list[User] | None = None,
                       documents: list[Document] | None = None
                       ) -> list[Notification]:
    raw = _load_raw(filename)
    if users is None:
        users = load_users()
    if documents is None:
        documents = load_documents(users=users)
    notifications = []
    for item in raw:
        note = Notification.from_data(item, users, documents)
        if note is not None:
            notifications.append(note)
    return notifications


def save_notifications(notifications: list[Notification],
                       filename: str = NOTIFICATIONS_FILE) -> None:
    _save_raw(filename, [note.to_dict() for note in notifications])
