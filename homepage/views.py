from django.http import HttpResponse


BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link href="{BOOTSTRAP_CSS}" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
  <div class="container">
    <a class="navbar-brand" href="/">Сервис напоминаний</a>
    <div class="navbar-nav">
      <a class="nav-link" href="/documents/">Документы</a>
      <a class="nav-link" href="/notifications/">Уведомления</a>
    </div>
  </div>
</nav>
<div class="container">
{content}
</div>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">Сервис напоминаний о сроках документов</h1>
    <p class="lead">Учёт документов и контроль сроков их действия.</p>
    <p>Основные разделы:</p>
    <a href="/documents/" class="btn btn-primary me-2">Документы</a>
    <a href="/notifications/" class="btn btn-secondary">Уведомления</a>
    """
    return HttpResponse(page("Сервис напоминаний", content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
