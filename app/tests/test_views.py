from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from app.models import CatModel


class CatViewSetTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="password"
        )

        self.cat = CatModel.objects.create(
            name="Test Cat", experience=5, salary=1000, breed="Siamese"
        )
        self.client = APIClient()

    def test_get_list_of_cats_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("app:catmodel-list")
        response = self.client.get(url)
        data = response.data["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.cat.name)

    def test_create_cat_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("app:catmodel-list")
        data = {
            "name": "New Cat",
            "experience": 2,
            "salary": 1000,
            "breed": "Siamese",
            "password": "password!5",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CatModel.objects.count(), 2)

    def test_create_cat_as_normal_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("app:catmodel-list")
        data = {
            "name": "New Cat",
            "experience": 2,
            "salary": 1000,
            "breed": "Siamese",
            "password": "password!5",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_cat_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("app:catmodel-detail", args=[self.cat.id])
        data = {"salary": 5}

        response = self.client.put(url, data, format="json")

        self.cat.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.cat.salary, 5)

    def test_update_cat_as_normal_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("app:catmodel-detail", args=[self.cat.id])
        data = {"salary": 5}

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_cat_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("app:catmodel-detail", args=[self.cat.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CatModel.objects.count(), 0)

    def test_permissions_for_create_and_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("app:catmodel-list")
        data = {
            "name": "New Cat",
            "experience": 1,
            "salary": 10,
            "breed": "Siamese",
            "password": "password!5",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
