from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lms.views import (
    LessonListCreateAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)

from lms.views import CourseViewSet

from lms.views import SubscriptionAPIView


router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "subscription/",
        SubscriptionAPIView.as_view(),
        name="subscription",
    ),
]

urlpatterns += [
    path("lessons/", LessonListCreateAPIView.as_view()),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view()),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view()),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view()),
]

