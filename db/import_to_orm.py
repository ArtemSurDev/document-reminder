import os
import sys
import sqlite3
from datetime import date
from pathlib import Path

import django

# Настраиваем пути, чтобы Django понял, где находится проект
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "document_reminder.settings")
django.setup()

# Импортируем наши новые модели Django
from users.models import User
from documents.models import Document
from notifications.models import Notification

# Путь к старой базе данных (из ПР7)
SOURCE_DB = BASE_DIR / "data" / "document_reminder.sqlite"


def main():
    if not SOURCE_DB.exists():
        print(f"Исходная база не найдена по пути: {SOURCE_DB}")
        return

    print("Начинаю перенос данных...")

    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row

        # 1. Переносим пользователей
        users = conn.execute("SELECT id, name, email FROM users").fetchall()
        for u in users:
            User.objects.update_or_create(
                pk=u["id"],
                defaults={"name": u["name"], "email": u["email"]}
            )

        # 2. Переносим документы
        docs = conn.execute("SELECT id, title, number, expiry, owner_id FROM documents").fetchall()
        for d in docs:
            Document.objects.update_or_create(
                pk=d["id"],
                defaults={
                    "title": d["title"],
                    "number": d["number"],
                    "expiry": date.fromisoformat(d["expiry"]),
                    "owner_id": d["owner_id"]
                }
            )

        # 3. Переносим уведомления
        notes = conn.execute("SELECT id, user_id, document_id, message, created FROM notifications").fetchall()
        for n in notes:
            Notification.objects.update_or_create(
                pk=n["id"],
                defaults={
                    "user_id": n["user_id"],
                    "document_id": n["document_id"],
                    "message": n["message"],
                    "created": date.fromisoformat(n["created"])
                }
            )

    print("=== ПЕРЕНОС ЗАВЕРШЕН ===")
    print(f"Пользователей в базе: {User.objects.count()}")
    print(f"Документов в базе: {Document.objects.count()}")
    print(f"Уведомлений в базе: {Notification.objects.count()}")


if __name__ == "__main__":
    main()