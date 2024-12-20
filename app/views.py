from django.http import HttpRequest
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

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

    @action(
        detail=True,
        methods=["GET"],
        url_path="assignats cat",
        url_name="assignats cat",
        permission_classes=[IsAdminUser],
    )
    def assignats_cat_to_mission(
        self, request: HttpRequest, pk: int = None
    ) -> Response:
        mission = self.get_object()
        cat_id = request.query_params.get("cat_id")

        if not cat_id:
            return Response(
                {"error": "Cat ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cat = CatModel.objects.get(id=cat_id)
        except CatModel.DoesNotExist:
            return Response(
                {"error": f"Cat with ID {cat_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if cat.missions.count() != 0:
            return Response(
                {
                    "error": "A cat can only be assigned to one mission at a time."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if mission.cat is not None:
            return Response(
                {
                    "error": f"Mission is already assigned to a cat - "
                             f"{mission.cat.name} (ID: {mission.cat.id})."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        mission.cat = cat
        mission.save()

        serializer = MissionListSerializer(mission)
        return Response(serializer.data)
