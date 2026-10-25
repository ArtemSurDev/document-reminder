from django.shortcuts import render

from models.notifications import find_notification_by_id
from storage import load_notifications


def notification_list(request):
    notes = load_notifications()
    context = {"notifications": notes}
    return render(request, "notifications/notification_list.html", context)


def notification_detail(request, notification_id):
    notes = load_notifications()
    note = find_notification_by_id(notes, notification_id)
    context = {"notification": note}
    return render(
        request,
        "notifications/notification_detail.html",
        context,
        status=404 if note is None else 200,
    )
