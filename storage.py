import json
import os


DATA_DIR = "data"
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.json")


def load_documents(filename: str = DOCUMENTS_FILE) -> list[dict]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, начинаем с пустого списка.")
        return []


def save_documents(documents: list[dict], filename: str = DOCUMENTS_FILE) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)
