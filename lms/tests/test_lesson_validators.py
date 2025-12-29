from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from lms.models import Course, Lesson


class LessonValidatorTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.ru", password="12345")
        self.course = Course.objects.create(title="Course", description="desc", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson_with_youtube_link(self):
        data = {
            "title": "Lesson YouTube",
            "description": "desc",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
        response = self.client.post("/api/lms/lessons/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_with_invalid_link(self):
        data = {
            "title": "Lesson Invalid",
            "description": "desc",
            "course": self.course.id,
            "video_url": "https://vimeo.com/123456"
        }
        response = self.client.post("/api/lms/lessons/create/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("video_url", response.data)
