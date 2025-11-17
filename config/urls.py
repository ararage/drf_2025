"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "", include(("watchmate.user_app.api.urls", "user_app"), namespace="user_app")
    ),
    path(
        "",
        include(
            ("watchmate.watchlist_app.api.urls", "watchlist_app"),
            namespace="watchlist_app",
        ),
    ),
]
