import json
import os


DATA_DIR = "data"
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, "notifications.json")


def _load(filename: str) -> list[dict]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, начинаем с пустого списка.")
        return []


def _save(filename: str, data: list[dict]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_documents(filename: str = DOCUMENTS_FILE) -> list[dict]:
    return _load(filename)


def save_documents(documents: list[dict],
                   filename: str = DOCUMENTS_FILE) -> None:
    _save(filename, documents)


def load_users(filename: str = USERS_FILE) -> list[dict]:
    return _load(filename)


def save_users(users: list[dict], filename: str = USERS_FILE) -> None:
    _save(filename, users)


def load_notifications(filename: str = NOTIFICATIONS_FILE) -> list[dict]:
    return _load(filename)


def save_notifications(notifications: list[dict],
                       filename: str = NOTIFICATIONS_FILE) -> None:
    _save(filename, notifications)
