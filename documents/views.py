from datetime import date
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from documents.models import Document


def document_list(request):
    documents = Document.objects.all()

    search_query = request.GET.get("q", "").strip()
    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query) | Q(number__icontains=search_query)
        )

    sort_by = request.GET.get("sort", "expiry")
    if sort_by == "title":
        documents = documents.order_by("title")
    else:
        documents = documents.order_by("expiry")

    return render(request, "documents/document_list.html", {"documents": documents})


def document_detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    return render(request, "documents/document_detail.html", {"document": document})


def available_documents(request):
    search_date = request.GET.get("date", "").strip()
    documents = []

    if search_date:
        try:
            selected_date = date.fromisoformat(search_date)
            documents = Document.objects.filter(expiry__gte=selected_date).order_by("expiry")
        except ValueError:
            pass

    return render(request, "documents/available.html", {
        "documents": documents,
        "search_date": search_date
    })