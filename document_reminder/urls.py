from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("documents/", include("documents.urls")),
    path("notifications/", include("notifications.urls")),
]

handler404 = "homepage.views.page_not_found"
