import requests
from django.contrib.auth.models import Group, Permission, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class AdminCSAModel(AbstractUser):
    is_staff = models.BooleanField(
        default=True,
    )
    groups = models.ManyToManyField(
        Group,
        related_name="admin_csa_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="admin_csa_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


class CatModel(AbstractUser):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the Cat Spy",
        db_comment="Name of the Cat Spy",
    )
    experience = models.PositiveIntegerField(
        default=0,
        help_text="Experience of the Cat Spy (in years)",
        db_comment="Experience of the Cat Spy (in years)",
    )
    breed = models.CharField(
        max_length=100,
        help_text="Breed of the Cat Spy",
        db_comment="Breed of the Cat Spy",
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Salary of the Cat Spy",
        db_comment="Salary of the Cat Spy",
    )

    groups = models.ManyToManyField(
        Group,
        related_name="cat_model_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="cat_model_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    username = None

    def clean(self):
        try:
            response = requests.get("https://api.thecatapi.com/v1/breeds")
            response_json = response.json()
            breed_list = [name["name"] for name in response_json]
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error fetching breed data: {e}")

        if self.breed not in breed_list:
            raise ValidationError(f"Invalid breed: {self.breed}")

        if self.salary <= 0:
            raise ValidationError("Salary must be a positive number.")
        if self.experience > 50:
            raise ValidationError("Experience seems unrealistically high.")

    def __str__(self):
        return self.name


class TargetModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)


class MissionModel(models.Model):
    cat = models.ForeignKey(
        CatModel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="missions",
    )
    targets = models.ManyToManyField(TargetModel, related_name="missions")
    completed = models.BooleanField(default=False)

    def check_and_complete_mission(self):
        if all(target.completed for target in self.targets.all()):
            self.completed = True
            self.save()

    def delete(self, *args, **kwargs):
        if self.cat:
            raise ValidationError(
                "Cannot delete a mission with a cat assigned."
            )
        super().delete(*args, **kwargs)
