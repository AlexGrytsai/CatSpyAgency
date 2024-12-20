from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import CatModel, TargetModel


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
