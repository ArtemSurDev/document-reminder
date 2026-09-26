from datetime import date

from models import User, Document, Notification
from models.notifications import (
    create_notification, add_notification,
)


def make_user():
    return User(1, "Иван Петров", "ivan@example.com")


def make_document():
    user = make_user()
    return Document(1, "Паспорт", "1", date(2026, 5, 20), user)


def test_notification_creation():
    user = make_user()
    doc = make_document()
    note = Notification(1, user, doc, "Тестовое сообщение")
    assert note.user is user
    assert note.document is doc
    assert note.message == "Тестовое сообщение"


def test_notification_str():
    user = make_user()
    doc = make_document()
    note = Notification(1, user, doc, "Напоминание")
    assert "Иван Петров" in str(note)
    assert "Напоминание" in str(note)


def test_notification_to_dict():
    user = make_user()
    doc = make_document()
    note = Notification(1, user, doc, "Напоминание")
    assert note.to_dict()["user_id"] == 1
    assert note.to_dict()["document_id"] == 1
    assert note.to_dict()["message"] == "Напоминание"


def test_create_notification():
    user = make_user()
    doc = make_document()
    note = create_notification(user, doc, "Сообщение")
    assert note.user is user
    assert note.document is doc


def test_add_notification():
    user = make_user()
    doc = make_document()
    notifications = []
    note = create_notification(user, doc, "Первое")
    add_notification(notifications, note)
    assert len(notifications) == 1
    assert notifications[0].id == 1


def test_add_multiple_notifications():
    user = make_user()
    doc = make_document()
    notifications = []
    add_notification(notifications, create_notification(user, doc, "Первое"))
    add_notification(notifications, create_notification(user, doc, "Второе"))
    assert len(notifications) == 2
    assert notifications[1].id == 2
