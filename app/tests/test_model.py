from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from app.models import CatModel, TargetModel, MissionModel


class CatModelTest(TestCase):
    @patch("requests.get")
    def test_cat_model_valid_breed(self, mock_get):
        mock_get.return_value.json.return_value = [{"name": "Siamese"},
                                                   {"name": "Persian"}]

        cat = CatModel(name="SpyCat", breed="Siamese", experience=5,
                       salary=1000)

        try:
            cat.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    @patch("requests.get")
    def test_cat_model_invalid_breed(self, mock_get):
        mock_get.return_value.json.return_value = [{"name": "Siamese"},
                                                   {"name": "Persian"}]

        cat = CatModel(name="SpyCat", breed="Bengal", experience=5,
                       salary=1000)

        with self.assertRaises(ValidationError):
            cat.clean()

    def test_invalid_salary(self):
        cat = CatModel(name="SpyCat", breed="Siamese", experience=5,
                       salary=-100)

        with self.assertRaises(ValidationError):
            cat.clean()

    def test_unrealistic_experience(self):
        cat = CatModel(name="SpyCat", breed="Siamese", experience=100,
                       salary=1000)

        with self.assertRaises(ValidationError):
            cat.clean()


class TargetModelTest(TestCase):
    def test_create_target_model(self):
        target = TargetModel.objects.create(name="Target1", country="Country1")
        self.assertEqual(target.name, "Target1")
        self.assertEqual(target.country, "Country1")
        self.assertFalse(target.completed)

    def test_target_notes(self):
        target = TargetModel.objects.create(name="Target2", country="Country2",
                                            notes="Important mission")
        self.assertEqual(target.notes, "Important mission")


class MissionModelTest(TestCase):
    def setUp(self):
        self.cat = CatModel.objects.create(name="SpyCat", breed="Siamese",
                                           experience=5, salary=1000)
        self.target1 = TargetModel.objects.create(name="Target1",
                                                  country="Country1")
        self.target2 = TargetModel.objects.create(name="Target2",
                                                  country="Country2")

    def test_create_mission_model(self):
        mission = MissionModel.objects.create(cat=self.cat)
        mission.targets.add(self.target1, self.target2)
        self.assertEqual(mission.cat, self.cat)
        self.assertEqual(mission.targets.count(), 2)
        self.assertFalse(mission.completed)

    def test_check_and_complete_mission(self):
        mission = MissionModel.objects.create(cat=self.cat)
        mission.targets.add(self.target1, self.target2)

        self.target1.completed = True
        self.target2.completed = True
        self.target1.save()
        self.target2.save()

        mission.check_and_complete_mission()
        self.assertTrue(mission.completed)

    def test_delete_mission_with_cat(self):
        mission = MissionModel.objects.create(cat=self.cat)
        mission.targets.add(self.target1)

        with self.assertRaises(ValidationError):
            mission.delete()

    def test_delete_mission_without_cat(self):
        mission = MissionModel.objects.create()
        mission.targets.add(self.target1)

        mission.delete()
        self.assertFalse(MissionModel.objects.filter(id=mission.id).exists())
