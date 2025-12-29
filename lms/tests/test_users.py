from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class UserCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.ru",
            password="12345",
            first_name="User"
        )
        self.other_user = User.objects.create_user(
            email="other@test.ru",
            password="12345",
            first_name="Other"
        )

    def test_registration(self):
        data = {"email": "new@test.ru", "password": "12345", "first_name": "New"}
        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="new@test.ru").exists())

    def test_login_jwt(self):
        data = {"email": "user@test.ru", "password": "12345"}
        response = self.client.post("/api/users/token/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_view_own_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_view_other_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/users/{self.other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.other_user.email)

    def test_update_own_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/users/{self.user.id}/", {"first_name": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_update_other_profile_forbidden(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/users/{self.other_user.id}/", {"first_name": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_other_profile_forbidden(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/users/{self.other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
