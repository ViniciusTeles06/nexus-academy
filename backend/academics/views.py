from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from accounts.models import User
from accounts.permissions import IsAdmin

from .models import (
    AcademicPeriod,
    ClassGroup,
    Course,
    Enrollment,
    Subject,
)
from .serializers import (
    AcademicPeriodSerializer,
    ClassGroupSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    SubjectSerializer,
)


class AdminWritePermissionMixin:
    """
    Usuários autenticados podem realizar consultas.
    Apenas administradores podem criar, alterar ou excluir.
    """

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.request.method not in SAFE_METHODS:
            permission_classes.append(IsAdmin)

        return [
            permission()
            for permission in permission_classes
        ]


class CourseViewSet(
    AdminWritePermissionMixin,
    viewsets.ModelViewSet,
):
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()

        if self.request.user.role == User.Role.ADMIN:
            return queryset

        return queryset.filter(is_active=True)


class AcademicPeriodViewSet(
    AdminWritePermissionMixin,
    viewsets.ModelViewSet,
):
    serializer_class = AcademicPeriodSerializer

    def get_queryset(self):
        queryset = AcademicPeriod.objects.all()

        if self.request.user.role == User.Role.ADMIN:
            return queryset

        return queryset.filter(is_active=True)


class SubjectViewSet(
    AdminWritePermissionMixin,
    viewsets.ModelViewSet,
):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        queryset = Subject.objects.select_related(
            "course",
        )

        if self.request.user.role == User.Role.ADMIN:
            return queryset

        return queryset.filter(
            is_active=True,
            course__is_active=True,
        )


class ClassGroupViewSet(
    AdminWritePermissionMixin,
    viewsets.ModelViewSet,
):
    serializer_class = ClassGroupSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = (
            ClassGroup.objects
            .select_related(
                "subject",
                "subject__course",
                "academic_period",
                "teacher",
                "teacher__user",
            )
        )

        if user.role == User.Role.ADMIN:
            return queryset

        if user.role == User.Role.TEACHER:
            return queryset.filter(
                teacher__user=user,
                is_active=True,
            )

        if user.role == User.Role.STUDENT:
            return queryset.filter(
                enrollments__student__user=user,
                enrollments__status=Enrollment.Status.ACTIVE,
                is_active=True,
            ).distinct()

        return queryset.none()


class EnrollmentViewSet(
    AdminWritePermissionMixin,
    viewsets.ModelViewSet,
):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = (
            Enrollment.objects
            .select_related(
                "student",
                "student__user",
                "student__course",
                "class_group",
                "class_group__subject",
                "class_group__academic_period",
                "class_group__teacher",
                "class_group__teacher__user",
            )
        )

        if user.role == User.Role.ADMIN:
            return queryset

        if user.role == User.Role.TEACHER:
            return queryset.filter(
                class_group__teacher__user=user,
            )

        if user.role == User.Role.STUDENT:
            return queryset.filter(
                student__user=user,
            )

        return queryset.none()