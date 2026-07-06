from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from lms.models import Course, Lesson


class UserManager(BaseUserManager):
    """Менеджер пользователей."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Город",
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Payment(models.Model):
    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHODS = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    payment_date = models.DateField(
        verbose_name="Дата оплаты",
    )

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный курс",
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный урок",
    )

    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default=TRANSFER,
        verbose_name="Способ оплаты",
    )

    def __str__(self):
        if self.paid_course:
            return f"{self.user} - {self.paid_course}"
        return f"{self.user} - {self.paid_lesson}"

