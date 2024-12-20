from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views import CatViewSet, MissionViewSet

router = DefaultRouter()

router.register("cats", CatViewSet)
router.register("missions", MissionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "app"
