from typing import List

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import CatModel, TargetModel, MissionModel


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatModel
        fields = ["id", "name", "password", "breed", "experience", "salary"]

        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "max_length": 128,
                "validators": [validate_password],
                "style": {"input_type": "password", "placeholder": "Password"},
            }
        }


class CatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatModel
        fields = ["salary"]


class TargetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetModel
        fields = ["name", "country"]


class TargetListSerializer(TargetModelSerializer):
    class Meta(TargetModelSerializer.Meta):
        fields = ["id", "name", "country", "completed", "notes"]


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetModel
        fields = ["id", "notes", "completed"]

    def validate_completed(self, value: bool) -> bool:
        if value:
            raise ValidationError("You cannot uncomplete a target.")
        return value

    def update(
        self, instance: TargetModel, validated_data: dict
    ) -> TargetModel:
        if instance.completed:
            raise ValidationError(
                "You cannot update the notes because the target is complete."
            )
        return super().update(instance, validated_data)


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetModelSerializer(many=True)

    class Meta:
        model = MissionModel
        fields = ["targets"]

    def validate_targets(self, value: List[TargetModel]) -> List[TargetModel]:
        if not (1 <= len(value) <= 3):
            raise serializers.ValidationError(
                "A mission must have between 1 and 3 targets."
            )
        return value

    def create(self, validated_data: dict) -> MissionModel:
        targets_data = validated_data.pop("targets")
        mission = MissionModel.objects.create(**validated_data)

        for target_data in targets_data:
            target = TargetModel.objects.create(**target_data)
            mission.targets.add(target)

        return mission


class MissionListSerializer(MissionSerializer):
    targets = TargetListSerializer(many=True, read_only=True)
    cat = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(MissionSerializer.Meta):
        fields = [
                     "id",
                     "cat",
                     "completed",
                 ] + MissionSerializer.Meta.fields


class MissionUpdateSerializer(serializers.ModelSerializer):
    targets = TargetUpdateSerializer(many=True, read_only=False)

    class Meta:
        model = MissionModel
        fields = ["completed", "targets"]

    def update(
        self, instance: MissionModel, validated_data: dict
    ) -> MissionModel:
        targets_data = self.initial_data.get("targets")

        if instance.completed:
            raise ValidationError("You cannot update a completed mission.")

        if targets_data:
            target_ids = []
            for target_data in targets_data:
                target_id = target_data.get("id")
                if not target_id:
                    raise ValidationError("Each target must have an 'id'.")

                try:
                    target = TargetModel.objects.get(id=target_id)
                except TargetModel.DoesNotExist:
                    raise ValidationError(
                        f"Target with id {target_id} does not exist."
                    )

                if target.completed:
                    raise ValidationError(
                        f"Target with id {target_id} is already completed "
                        f"and cannot be updated."
                    )
                serializer = TargetUpdateSerializer(
                    instance=target, data=target_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

                target_ids.append(target)

            instance.targets.set(target_ids)

        for attr, value in validated_data.items():
            if attr != "targets":
                setattr(instance, attr, value)
        instance.save()

        return instance
