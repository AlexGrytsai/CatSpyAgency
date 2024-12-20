from django.http import HttpRequest
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from app.models import CatModel, MissionModel
from app.permissions import IsAdminOrCatAssigned
from app.serializers import (
    CatSerializer,
    CatUpdateSerializer,
    MissionSerializer,
    MissionListSerializer,
    MissionUpdateSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List all spy cats",
        description="Retrieve a list of all cats.",
        tags=["Cats"],
    ),
    create=extend_schema(
        summary="Create a new spy cat",
        description="Create a new cat. Need to be admin.",
        tags=["Cats"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific spy cat",
        description="Retrieve a specific cat by ID.",
        tags=["Cats"],
    ),
    update=extend_schema(
        summary="Update a specific spy cat",
        description="Update a cat's details. Need to be admin.",
        tags=["Cats"],
    ),
    partial_update=extend_schema(
        summary="Partially update a specific spy cat",
        description="Partially update a cat's details. Need to be admin.",
        tags=["Cats"],
    ),
    destroy=extend_schema(
        summary="Delete a specific spy cat",
        description="Delete a specific cat. Need to be admin.",
        tags=["Cats"],
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="List all missions",
        description="Retrieve a list of all missions.",
        tags=["Missions"],
    ),
    create=extend_schema(
        summary="Create a new mission",
        description="Create a new mission. Need to be admin.",
        tags=["Missions"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific mission",
        description="Retrieve a specific mission by ID.",
        tags=["Missions"],
    ),
    update=extend_schema(
        summary="Update a specific mission",
        description="Update a mission's details. "
        "Need to be admin or cat assigned.",
        tags=["Missions"],
    ),
    partial_update=extend_schema(
        summary="Partially update a specific mission",
        description="Partially update a mission's details. "
        "Need to be admin or cat assigned.",
        tags=["Missions"],
    ),
    destroy=extend_schema(
        summary="Delete a specific mission",
        description="Delete a specific mission. Need to be admin.",
        tags=["Missions"],
    ),
    assignats_cat_to_mission=extend_schema(
        summary="Assign a cat to a mission",
        description="Assign a cat to a mission. Need to be admin.",
        tags=["Missions"],
        responses={
            200: MissionListSerializer,
            400: OpenApiResponse(
                description="Bad Request, missing or invalid data"
            ),
            404: OpenApiResponse(description="Cat not found"),
        },
    ),
    finish_mission=extend_schema(
        summary="Finish a mission",
        description="Finish a mission and unassign the cat. Need to be admin.",
        tags=["Missions"],
        responses={
            200: OpenApiResponse(description="Mission completed"),
        },
    ),
)
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

    @action(
        detail=True,
        methods=["GET"],
        url_path="finish mission",
        url_name="finish mission",
        permission_classes=[IsAdminUser],
    )
    def finish_mission(self, request: HttpRequest, pk: int = None) -> Response:
        mission: MissionModel = self.get_object()

        if not mission.completed:
            mission.completed = True
            mission.cat = None
            mission.save()

        return Response(
            {"success": "Mission completed."}, status=status.HTTP_200_OK
        )
