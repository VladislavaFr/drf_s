from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import Group

from users.models import User
from lms.models import Course, Lesson


class ModeratorPermissionTestCase(APITestCase):
    def setUp(self):
        # создаем группу модераторов
        self.moder_group, _ = Group.objects.get_or_create(name="moderators")

        self.user = User.objects.create_user(email="user@test.ru", password="12345")
        self.moder = User.objects.create_user(email="moder@test.ru", password="12345")
        self.moder.groups.add(self.moder_group)

        self.course = Course.objects.create(title="Course", description="desc", owner=self.user)
        self.lesson = Lesson.objects.create(title="Lesson", description="desc", course=self.course, owner=self.user)

    def test_moderator_can_view_any_lesson(self):
        self.client.force_authenticate(user=self.moder)
        response = self.client.get(f"/api/lms/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_can_update_any_lesson(self):
        self.client.force_authenticate(user=self.moder)
        response = self.client.patch(f"/api/lms/lessons/{self.lesson.id}/update/", {"title": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moder)
        response = self.client.delete(f"/api/lms/lessons/{self.lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.moder)
        response = self.client.post("/api/lms/lessons/create/", {
            "title": "New Lesson",
            "description": "desc",
            "course": self.course.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
