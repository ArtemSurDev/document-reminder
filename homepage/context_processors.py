from documents.models import Document


def global_context(request):
    return {
        "site_name": "Сервис напоминаний",
        "documents_count": Document.objects.count(),
    }
