from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("app.urls")),
] + debug_toolbar_urls()
