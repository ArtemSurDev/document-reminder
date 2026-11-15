from django.contrib import admin
from .models import User
from documents.models import Document


class DocumentInline(admin.TabularInline):
    model = Document
    fields = ("title", "number", "expiry")
    extra = 0
    can_delete = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    list_display_links = ("name",)
    search_fields = ("name", "email")
    ordering = ("name",)
    list_per_page = 20
    inlines = (DocumentInline,)