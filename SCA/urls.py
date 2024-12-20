from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView, TokenVerifyView

urlpatterns = [
path(
        "api/v1/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path(
        "api/v1/token/logout/",
        LogoutView.as_view(),
        name="token_logout",
    ),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/v1/", include("app.urls")),
] + debug_toolbar_urls()
