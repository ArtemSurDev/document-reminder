import os
import tempfile

from storage import load_documents, save_documents


def test_save_and_load():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.json")
        docs = [{"id": 1, "title": "Тест", "number": "1", "expiry": "2026-01-01"}]
        save_documents(docs, path)
        loaded = load_documents(path)
        assert loaded == docs


def test_load_missing_file():
    assert load_documents("nonexistent.json") == []


def test_load_broken_json():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{broken")
        path = f.name
    try:
        assert load_documents(path) == []
    finally:
        os.unlink(path)
