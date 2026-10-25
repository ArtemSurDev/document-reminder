import json
from db.database import get_connection

USERS_FILE = "data/users.json"
DOCUMENTS_FILE = "data/documents.json"
NOTIFICATIONS_FILE = "data/notifications.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_users(conn):
    users = load_json(USERS_FILE)
    conn.executemany(
        "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
        [(u["id"], u["name"], u["email"]) for u in users]
    )


def import_documents(conn):
    documents = load_json(DOCUMENTS_FILE)
    conn.executemany(
        "INSERT INTO documents (id, title, number, expiry, owner_id) "
        "VALUES (?, ?, ?, ?, ?)",
        [(d["id"], d["title"], d["number"], d["expiry"], d["owner_id"])
         for d in documents]
    )


def import_notifications(conn):
    notifications = load_json(NOTIFICATIONS_FILE)
    conn.executemany(
        "INSERT INTO notifications (id, user_id, document_id, message, created) "
        "VALUES (?, ?, ?, ?, ?)",
        [(n["id"], n["user_id"], n["document_id"], n["message"], n["created"])
         for n in notifications]
    )


def main():
    conn = get_connection()
    try:
        import_users(conn)
        import_documents(conn)
        import_notifications(conn)
        conn.commit()
        print("Данные успешно импортированы!")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
