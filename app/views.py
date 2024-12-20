from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app.models import CatModel
from app.serializers import CatSerializer, CatUpdateSerializer


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
