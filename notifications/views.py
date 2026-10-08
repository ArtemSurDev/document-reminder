from django.http import HttpResponse

from homepage.views import page
from models.notifications import find_notification_by_id
from storage import load_notifications


def notifications(request):
    notes = load_notifications()
    items = ""
    for note in notes:
        items += (
            f'<li class="list-group-item">'
            f'<a href="/notifications/{note.id}/">'
            f'{note.created} — {note.document.title}'
            f'</a> '
            f'<span class="text-muted">{note.user.name}</span>'
            f'</li>'
        )
    content = f"""
    <h1>Уведомления</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Уведомления", content))


def notification_detail(request, notification_id: int):
    notes = load_notifications()
    note = find_notification_by_id(notes, notification_id)
    if note is None:
        content = """
        <h1 class="text-danger">Уведомление не найдено</h1>
        <a href="/notifications/" class="btn btn-outline-secondary">
            ← к списку уведомлений
        </a>
        """
        return HttpResponse(
            page("Уведомление не найдено", content),
            status=404,
        )

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Уведомление №{note.id}</h5>
        <p class="card-text"><strong>Дата:</strong> {note.created}</p>
        <p class="card-text"><strong>Пользователь:</strong> {note.user.name}</p>
        <p class="card-text"><strong>Документ:</strong> {note.document.title}</p>
        <p class="card-text"><strong>Сообщение:</strong> {note.message}</p>
        <a href="/notifications/" class="btn btn-outline-secondary">
            ← к списку уведомлений
        </a>
      </div>
    </div>
    """
    return HttpResponse(page("Уведомление", content))
