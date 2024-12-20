from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app.models import CatModel, MissionModel
from app.permissions import IsAdminOrCatAssigned
from app.serializers import CatSerializer, CatUpdateSerializer, \
    MissionSerializer, MissionListSerializer, MissionUpdateSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = CatModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CatSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "delete"):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            self.serializer_class = CatUpdateSerializer
        return super().get_serializer_class()


class MissionViewSet(viewsets.ModelViewSet):
    queryset = (
        MissionModel.objects.all()
        .select_related("cat")
        .prefetch_related("targets")
    )
    permission_classes = (IsAuthenticated,)
    serializer_class = MissionSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update"):
            self.permission_classes = (IsAdminOrCatAssigned,)
        if self.action in ("create", "delete"):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            self.serializer_class = MissionListSerializer
        elif self.action in ("update", "partial_update"):
            return MissionUpdateSerializer
        return super().get_serializer_class()
