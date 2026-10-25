from datetime import date
from django.shortcuts import render

from models.documents import find_document_by_id
from storage import load_documents


def document_list(request):
    docs = load_documents()
    today = date.today()
    for doc in docs:
        days_left = doc.days_until_expiry(today)
        doc.days_left = days_left
        doc.status = doc.get_status(days_left)

    context = {"documents": docs}
    return render(request, "documents/document_list.html", context)


def document_detail(request, document_id):
    docs = load_documents()
    doc = find_document_by_id(docs, document_id)

    if doc is not None:
        today = date.today()
        days_left = doc.days_until_expiry(today)
        doc.days_left = days_left
        doc.status = doc.get_status(days_left)

    context = {"document": doc}
    return render(
        request,
        "documents/document_detail.html",
        context,
        status=404 if doc is None else 200,
    )
