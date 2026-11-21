from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Document
from .forms import DocumentForm, DocumentFilterForm


def document_list(request):
    documents = Document.objects.all()
    form = DocumentFilterForm(request.GET)

    if form.is_valid():
        expiry_date = form.cleaned_data.get("expiry_date")
        owner = form.cleaned_data.get("owner")

        if expiry_date:
            documents = documents.filter(expiry__gte=expiry_date)
        if owner:
            documents = documents.filter(owner=owner)

    search_query = request.GET.get("q", "").strip()
    if search_query:
        documents = documents.filter(Q(title__icontains=search_query) | Q(number__icontains=search_query))

    return render(request, "documents/document_list.html", {"documents": documents, "form": form})


def document_detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    return render(request, "documents/document_detail.html", {"document": document})


def document_create(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("documents:list")
    else:
        form = DocumentForm()

    return render(request, "documents/document_form.html", {"form": form, "title": "Добавить документ"})


def document_edit(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect("documents:detail", document_id=document.id)
    else:
        form = DocumentForm(instance=document)

    return render(request, "documents/document_form.html", {"form": form, "title": "Редактировать документ"})


def document_delete(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == "POST":
        document.delete()
        return redirect("documents:list")
    return render(request, "documents/document_confirm_delete.html", {"document": document})


def available_documents(request):
    search_date = request.GET.get("date", "").strip()
    documents = []
    if search_date:
        try:
            selected_date = date.fromisoformat(search_date)
            documents = Document.objects.filter(expiry__gte=selected_date).order_by("expiry")
        except ValueError:
            pass
    return render(request, "documents/available.html", {"documents": documents, "search_date": search_date})
