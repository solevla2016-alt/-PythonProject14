from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from lms.models import Course, Subscription


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="12345",
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name="Python",
            description="Python course",
            owner=self.user,
        )

    def test_subscribe(self):
        """Проверка создания подписки"""

        response = self.client.post(
            "/lms/subscription/",
            {"course_id": self.course.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Подписка добавлена",
        )

        self.assertEqual(
            Subscription.objects.count(),
            1,
        )

    def test_unsubscribe(self):
        """Проверка удаления подписки"""

        Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

        response = self.client.post(
            "/lms/subscription/",
            {"course_id": self.course.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Подписка удалена",
        )

        self.assertEqual(
            Subscription.objects.count(),
            0,
        )