from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.document_list, name="list"),
    path("add/", views.document_create, name="create"),
    path("<int:document_id>/", views.document_detail, name="detail"),
    path("<int:document_id>/edit/", views.document_edit, name="edit"),
    path("<int:document_id>/delete/", views.document_delete, name="delete"),
    path("available/", views.available_documents, name="available"),
]
