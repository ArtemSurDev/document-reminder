from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "document", "created")
    list_display_links = ("id",)
    search_fields = ("user__name", "document__title", "message")
    list_filter = ("created", "user")
    ordering = ("-created",)
    list_per_page = 20
    readonly_fields = ("id",)
    list_select_related = ("user", "document")