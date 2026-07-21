from django.db import models
from django.conf import settings


class Course(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )

    preview = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True,
        verbose_name="Превью",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    def __str__(self):
        return self.name





class Lesson(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )


    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    preview = models.ImageField(
        upload_to="lessons/",
        blank=True,
        null=True,
        verbose_name="Превью",
    )

    video_link = models.URLField(
        blank=True,
        verbose_name="Ссылка на видео",
    )

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )

    def __str__(self):
        return f"{self.user} - {self.course}"



    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="unique_user_course_subscription",
            )
        ]
