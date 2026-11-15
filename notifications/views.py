from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from users.models import User
from notifications.models import Notification


def notification_list(request):
    notifications = Notification.objects.select_related("user", "document").all()
    return render(request, "notifications/notification_list.html", {"notifications": notifications})


def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    return render(request, "notifications/notification_detail.html", {"notification": notification})


def statistics(request):
    users_stats = User.objects.annotate(
        doc_count=Count("documents")
    ).order_by("-doc_count")

    return render(request, "notifications/statistics.html", {"stats": users_stats})
