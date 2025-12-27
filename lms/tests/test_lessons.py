from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from lms.models import Course, Lesson


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.ru",
            password="12345"
        )
        self.other_user = User.objects.create_user(
            email="other@test.ru",
            password="12345"
        )

        self.course = Course.objects.create(
            title="Test course",
            description="desc",
            owner=self.user,
        )

        self.lesson = Lesson.objects.create(
            title="Test lesson",
            description="desc",
            course=self.course,
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            "title": "New lesson",
            "description": "desc",
            "course": self.course.id,
        }
        response = self.client.post("/api/lms/lessons/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_lesson(self):
        response = self.client.get(f"/api/lms/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        data = {"title": "Updated"}
        response = self.client.patch(
            f"/api/lms/lessons/{self.lesson.id}/update/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        response = self.client.delete(
            f"/api/lms/lessons/{self.lesson.id}/delete/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_foreign_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(
            f"/api/lms/lessons/{self.lesson.id}/delete/"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
