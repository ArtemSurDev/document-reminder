from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "number", "expiry", "owner")
    list_display_links = ("title",)
    search_fields = ("title", "number", "owner__name")
    list_filter = ("expiry", "owner")
    ordering = ("-expiry",)
    list_per_page = 20
    readonly_fields = ("id",)