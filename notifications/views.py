import sqlite3
from django.shortcuts import render

DB_PATH = "data/document_reminder.sqlite"


def notification_list(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    notifications = conn.execute("""
        SELECT notifications.id, notifications.message, notifications.created,
               users.name AS user_name, documents.title AS doc_title
        FROM notifications
        JOIN users ON notifications.user_id = users.id
        JOIN documents ON notifications.document_id = documents.id
        ORDER BY notifications.created DESC
    """).fetchall()
    conn.close()

    return render(request, "notifications/notification_list.html",
                  {"notifications": notifications})


def notification_detail(request, notification_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    notification = conn.execute("""
        SELECT notifications.id, notifications.message, notifications.created,
               users.name AS user_name, documents.title AS doc_title
        FROM notifications
        JOIN users ON notifications.user_id = users.id
        JOIN documents ON notifications.document_id = documents.id
        WHERE notifications.id = ?
    """, (notification_id,)).fetchone()
    conn.close()

    return render(
        request,
        "notifications/notification_detail.html",
        {"notification": notification},
        status=404 if notification is None else 200,
    )


def statistics(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    stats = conn.execute("""
        SELECT users.name AS user_name, COUNT(documents.id) AS doc_count
        FROM users
        LEFT JOIN documents ON users.id = documents.owner_id
        GROUP BY users.id, users.name
        ORDER BY doc_count DESC
    """).fetchall()
    conn.close()

    return render(request, "notifications/statistics.html", {"stats": stats})
