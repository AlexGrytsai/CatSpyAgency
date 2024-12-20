from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from app.models import CatModel


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
