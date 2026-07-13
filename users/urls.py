from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import (
    RegisterAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    PaymentListAPIView,
)

urlpatterns = [
    # Регистрация
    path("register/", RegisterAPIView.as_view(), name="register"),

    # JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Пользователи
    path("", UserListAPIView.as_view(), name="users_list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="users_detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="users_update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="users_delete"),

    # Платежи
    path("payments/", PaymentListAPIView.as_view(), name="payments"),
]