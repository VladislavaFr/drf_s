from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from lms.models import Course, Subscription


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sub@test.ru",
            password="12345"
        )

        self.course = Course.objects.create(
            title="Course",
            description="desc",
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        response = self.client.post(
            "/api/lms/subscriptions/",
            {"course_id": self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe(self):
        Subscription.objects.create(user=self.user, course=self.course)

        response = self.client.post(
            "/api/lms/subscriptions/",
            {"course_id": self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
