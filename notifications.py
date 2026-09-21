from datetime import date


def create_notification(user_id: int, document_id: int,
                        message: str) -> dict:
    return {
        "id": None,
        "user_id": user_id,
        "document_id": document_id,
        "message": message,
        "created": date.today().isoformat(),
    }


def add_notification(notifications: list[dict],
                     notification: dict) -> dict:
    notification["id"] = len(notifications) + 1
    notifications.append(notification)
    return notification
