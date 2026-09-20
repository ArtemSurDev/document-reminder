from datetime import date
import pytest

from documents import (
    add_document, find_documents, days_until_expiry,
    get_status, format_notification, get_expiring_documents,
    sort_documents_by_expiry, get_statistics,
)


def test_add_document():
    docs = []
    add_document(docs, "Паспорт РФ", "1234", date(2026, 5, 20))
    assert len(docs) == 1
    assert docs[0]["title"] == "Паспорт РФ"


def test_find_documents():
    docs = []
    add_document(docs, "Паспорт РФ", "1234", date(2026, 5, 20))
    add_document(docs, "Водительские права", "5678", date(2026, 10, 15))
    found = find_documents(docs, "паспорт")
    assert len(found) == 1
    assert found[0]["title"] == "Паспорт РФ"


def test_days_until_expiry():
    assert days_until_expiry(date(2026, 5, 20), date(2026, 4, 25)) == 25


def test_get_status():
    assert get_status(-5) == "ПРОСРОЧЕН"
    assert get_status(0) == "ИСТЕКАЕТ СЕГОДНЯ"
    assert get_status(25) == "ИСТЕКАЕТ СКОРО"
    assert get_status(100) == "ДЕЙСТВИТЕЛЕН"


def test_format_notification():
    result = format_notification("Иван", "Паспорт РФ", 25)
    assert "25 дн." in result


def test_get_expiring_documents():
    docs = []
    add_document(docs, "Страховка", "9999", date.today())
    expiring = get_expiring_documents(docs, threshold=30)
    assert len(expiring) == 1


def test_sort_documents_by_expiry():
    docs = []
    add_document(docs, "B", "1", date(2027, 1, 1))
    add_document(docs, "A", "2", date(2026, 1, 1))
    sorted_docs = sort_documents_by_expiry(docs)
    assert sorted_docs[0]["title"] == "A"


def test_get_statistics():
    docs = []
    add_document(docs, "A", "1", date(2020, 1, 1))  # просрочен
    stats = get_statistics(docs)
    assert stats["total"] == 1
    assert stats["expired"] == 1