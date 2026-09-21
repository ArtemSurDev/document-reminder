from datetime import date


def add_document(documents: list[dict], title: str, number: str,
                 expiry: date, owner_id: int = 1) -> dict:
    doc_id = len(documents) + 1
    doc = {
        "id": doc_id,
        "title": title,
        "number": number,
        "expiry": expiry.isoformat(),
        "owner_id": owner_id,
    }
    documents.append(doc)
    return doc


def find_documents(documents: list[dict], query: str) -> list[dict]:
    result = []
    for doc in documents:
        if query.lower() in doc["title"].lower():
            result.append(doc)
    return result


def days_until_expiry(expiry: date, current: date) -> int:
    return (expiry - current).days


def get_status(days_left: int) -> str:
    if days_left < 0:
        return "ПРОСРОЧЕН"
    elif days_left == 0:
        return "ИСТЕКАЕТ СЕГОДНЯ"
    elif days_left <= 30:
        return "ИСТЕКАЕТ СКОРО"
    else:
        return "ДЕЙСТВИТЕЛЕН"


def format_notification(user: str, title: str, days_left: int) -> str:
    if days_left < 0:
        return f"{user}, документ «{title}» просрочен на {abs(days_left)} дн."
    return f"{user}, до окончания «{title}» осталось {days_left} дн."


def get_expiring_documents(documents: list[dict],
                           threshold: int = 30) -> list[dict]:
    today = date.today()
    result = []
    for doc in documents:
        expiry = date.fromisoformat(doc["expiry"])
        days_left = days_until_expiry(expiry, today)
        if days_left <= threshold:
            result.append({**doc, "days_left": days_left})
    return result


def sort_documents_by_expiry(documents: list[dict]) -> list[dict]:
    return sorted(documents, key=lambda d: d["expiry"])


def get_statistics(documents: list[dict]) -> dict:
    today = date.today()
    stats = {"total": len(documents), "expired": 0, "expiring": 0, "valid": 0}
    for doc in documents:
        expiry = date.fromisoformat(doc["expiry"])
        days_left = days_until_expiry(expiry, today)
        if days_left < 0:
            stats["expired"] += 1
        elif days_left <= 30:
            stats["expiring"] += 1
        else:
            stats["valid"] += 1
    return stats
