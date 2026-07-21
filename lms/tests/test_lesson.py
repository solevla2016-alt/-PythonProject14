from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from lms.models import Course, Lesson


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="12345"
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name="Python",
            description="Python course",
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name="Lesson 1",
            description="Test lesson",
            course=self.course,
            owner=self.user
        )

    def test_lesson_list(self):
        response = self.client.get("/lms/lessons/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_lesson_create(self):

        data = {
            "name": "Lesson 2",
            "description": "New lesson",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=test"
        }

        response = self.client.post(
            "/lms/lessons/",
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.count(),
            2
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            f"/lms/lessons/{self.lesson.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["name"],
            self.lesson.name
        )

    def test_lesson_update(self):
        data = {
            "name": "Updated lesson",
            "description": "Updated description",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=test",
        }

        response = self.client.put(
            f"/lms/lessons/{self.lesson.pk}/update/",
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.lesson.refresh_from_db()

        self.assertEqual(
            self.lesson.name,
            "Updated lesson"
        )

    def test_lesson_delete(self):
        response = self.client.delete(
            f"/lms/lessons/{self.lesson.pk}/delete/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.count(),
            0
        )

    def test_invalid_video_link(self):
        """Проверка, что можно использовать только ссылки на YouTube"""

        data = {
            "name": "Урок",
            "description": "Описание",
            "course": self.course.id,
            "video_link": "https://skillbox.ru/python",
        }

        response = self.client.post(
            "/lms/lessons/",
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "non_field_errors",
            response.data,
        )

        self.assertEqual(
            response.data["non_field_errors"][0],
            "Разрешены только ссылки на youtube.com",
        )