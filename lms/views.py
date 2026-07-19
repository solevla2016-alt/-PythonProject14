from rest_framework import viewsets

from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer

from rest_framework import generics

from lms.serializers import LessonSerializer

from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModerator
from lms.permissions import IsOwner

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from lms.paginators import LMSPagination





class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LMSPagination

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all().order_by("id")

        return Lesson.objects.filter(owner=self.request.user).order_by("id")


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LMSPagination

    def get_permissions(self):

        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]

        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]

        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [
                IsAuthenticated,
                IsModerator | IsOwner,
            ]

        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Course.objects.all().order_by("id")

        return Course.objects.filter(owner=self.request.user).order_by("id")

class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")

        course = get_object_or_404(
            Course,
            pk=course_id
        )

        subscription = Subscription.objects.filter(
            user=user,
            course=course
        )

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(
                user=user,
                course=course
            )
            message = "Подписка добавлена"

        return Response(
            {"message": message}
        )

