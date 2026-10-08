from datetime import date

from django.http import HttpResponse

from homepage.views import page
from models.documents import find_document_by_id
from storage import load_documents


def documents(request):
    docs = load_documents()
    today = date.today()
    items = ""
    for doc in docs:
        days_left = doc.days_until_expiry(today)
        status = doc.get_status(days_left)
        items += (
            f'<li class="list-group-item d-flex justify-content-between">'
            f'<a href="/documents/{doc.id}/">{doc.title} — до {doc.expiry}</a>'
            f'<span class="badge bg-info">{status}</span>'
            f'</li>'
        )
    content = f"""
    <h1>Документы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Документы", content))


def document_detail(request, document_id: int):
    docs = load_documents()
    doc = find_document_by_id(docs, document_id)
    if doc is None:
        content = """
        <h1 class="text-danger">Документ не найден</h1>
        <a href="/documents/" class="btn btn-outline-secondary">
            ← к списку документов
        </a>
        """
        return HttpResponse(
            page("Документ не найден", content),
            status=404,
        )

    today = date.today()
    days_left = doc.days_until_expiry(today)
    status = doc.get_status(days_left)
    badge = "bg-success" if days_left > 30 else "bg-warning"
    if days_left < 0:
        badge = "bg-danger"

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{doc.title}</h5>
        <p class="card-text"><strong>Номер:</strong> {doc.number}</p>
        <p class="card-text"><strong>Владелец:</strong> {doc.owner.name}</p>
        <p class="card-text"><strong>Действителен до:</strong> {doc.expiry}</p>
        <p class="card-text">
          <strong>До окончания:</strong> {days_left} дн.
          <span class="badge {badge}">{status}</span>
        </p>
        <a href="/documents/" class="btn btn-outline-secondary">
            ← к списку документов
        </a>
      </div>
    </div>
    """
    return HttpResponse(page(doc.title, content))
