from datetime import date

from models import User, Document
from models.documents import (
    add_document, find_documents, get_expiring_documents,
    sort_documents_by_expiry, get_statistics, find_document_by_id,
)


def make_user():
    return User(1, "Иван Петров", "ivan@example.com")


def test_document_creation():
    user = make_user()
    doc = Document(1, "Паспорт РФ", "1234", date(2026, 5, 20), user)
    assert doc.id == 1
    assert doc.title == "Паспорт РФ"
    assert doc.expiry == date(2026, 5, 20)
    assert doc.owner is user


def test_document_days_until_expiry():
    user = make_user()
    doc = Document(1, "Паспорт", "1", date(2026, 5, 20), user)
    assert doc.days_until_expiry(date(2026, 4, 25)) == 25


def test_document_get_status():
    user = make_user()
    doc = Document(1, "Паспорт", "1", date(2026, 5, 20), user)
    assert doc.get_status(-5) == "ПРОСРОЧЕН"
    assert doc.get_status(0) == "ИСТЕКАЕТ СЕГОДНЯ"
    assert doc.get_status(25) == "ИСТЕКАЕТ СКОРО"
    assert doc.get_status(100) == "ДЕЙСТВИТЕЛЕН"


def test_document_format_notification():
    user = make_user()
    doc = Document(1, "Паспорт", "1", date(2026, 5, 20), user)
    result = doc.format_notification(25)
    assert "25 дн." in result
    assert "Паспорт" in result


def test_document_from_data():
    user = make_user()
    users = [user]
    data = {"id": 1, "title": "Паспорт", "number": "1",
            "expiry": "2026-05-20", "owner_id": 1}
    doc = Document.from_data(data, users)
    assert doc is not None
    assert doc.owner is user


def test_document_to_dict():
    user = make_user()
    doc = Document(1, "Паспорт", "1", date(2026, 5, 20), user)
    assert doc.to_dict() == {
        "id": 1,
        "title": "Паспорт",
        "number": "1",
        "expiry": "2026-05-20",
        "owner_id": 1,
    }


def test_add_document():
    user = make_user()
    docs = []
    add_document(docs, "Паспорт", "1", date(2026, 5, 20), user)
    assert len(docs) == 1
    assert isinstance(docs[0], Document)


def test_find_documents():
    user = make_user()
    docs = []
    add_document(docs, "Паспорт РФ", "1", date(2026, 5, 20), user)
    add_document(docs, "Права", "2", date(2026, 10, 15), user)
    found = find_documents(docs, "паспорт")
    assert len(found) == 1
    assert found[0].title == "Паспорт РФ"


def test_find_document_by_id():
    user = make_user()
    docs = []
    add_document(docs, "Паспорт", "1", date(2026, 5, 20), user)
    assert find_document_by_id(docs, 1) is not None
    assert find_document_by_id(docs, 99) is None


def test_get_expiring_documents():
    user = make_user()
    docs = []
    add_document(docs, "Страховка", "1", date.today(), user)
    assert len(get_expiring_documents(docs, threshold=30)) == 1


def test_sort_documents_by_expiry():
    user = make_user()
    docs = []
    add_document(docs, "B", "1", date(2027, 1, 1), user)
    add_document(docs, "A", "2", date(2026, 1, 1), user)
    sorted_docs = sort_documents_by_expiry(docs)
    assert sorted_docs[0].title == "A"


def test_get_statistics():
    user = make_user()
    docs = []
    add_document(docs, "A", "1", date(2020, 1, 1), user)
    stats = get_statistics(docs)
    assert stats["total"] == 1
    assert stats["expired"] == 1
