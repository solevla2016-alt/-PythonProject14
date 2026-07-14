from rest_framework import viewsets

from lms.models import Course
from lms.serializers import CourseSerializer

from rest_framework import generics

from lms.models import Lesson
from lms.serializers import LessonSerializer

from rest_framework.permissions import IsAuthenticated

from lms.permissions import IsModerator, IsOwner




class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

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
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


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
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)

