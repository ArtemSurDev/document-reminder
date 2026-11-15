from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("documents/", include("documents.urls")),
    path("notifications/", include("notifications.urls")),
]

handler404 = "homepage.views.page_not_found"

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
