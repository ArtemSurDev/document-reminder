from notifications import create_notification, add_notification


def test_create_notification():
    note = create_notification(1, 1, "Тестовое сообщение")
    assert note["user_id"] == 1
    assert note["document_id"] == 1
    assert note["message"] == "Тестовое сообщение"
    assert "created" in note


def test_create_notification_id_is_none():
    note = create_notification(1, 1, "Сообщение")
    assert note["id"] is None


def test_add_notification():
    notifications = []
    note = create_notification(1, 1, "Сообщение")
    add_notification(notifications, note)
    assert len(notifications) == 1
    assert notifications[0]["id"] == 1


def test_add_multiple_notifications():
    notifications = []
    add_notification(notifications, create_notification(1, 1, "Первое"))
    add_notification(notifications, create_notification(1, 2, "Второе"))
    assert len(notifications) == 2
    assert notifications[0]["id"] == 1
    assert notifications[1]["id"] == 2


def test_notification_message_saved():
    notifications = []
    note = create_notification(1, 1, "Важное уведомление")
    add_notification(notifications, note)
    assert notifications[0]["message"] == "Важное уведомление"
