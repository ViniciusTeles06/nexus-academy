from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from accounts.models import User

from .models import AttendanceRecord, ClassSession
from .serializers import (
    AttendanceRecordSerializer,
    ClassSessionSerializer,
)


class ClassSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ClassSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = ClassSession.objects.select_related(
            "class_group",
            "class_group__subject",
            "class_group__academic_period",
            "class_group__teacher",
            "class_group__teacher__user",
        )

        if user.role == User.Role.ADMIN:
            return queryset

        if user.role == User.Role.TEACHER:
            return queryset.filter(
                class_group__teacher__user=user,
            )

        if user.role == User.Role.STUDENT:
            return queryset.filter(
                class_group__enrollments__student__user=user,
                class_group__enrollments__status="ACTIVE",
            ).distinct()

        return queryset.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            serializer.save()
            return

        if user.role != User.Role.TEACHER:
            raise PermissionDenied(
                "Apenas professores e administradores "
                "podem criar aulas."
            )

        class_group = serializer.validated_data["class_group"]

        if class_group.teacher.user_id != user.id:
            raise PermissionDenied(
                "Você só pode criar aulas "
                "nas suas próprias turmas."
            )

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        session = self.get_object()

        if user.role == User.Role.ADMIN:
            serializer.save()
            return

        if (
            user.role != User.Role.TEACHER
            or session.class_group.teacher.user_id != user.id
        ):
            raise PermissionDenied(
                "Você não pode alterar esta aula."
            )

        new_class_group = serializer.validated_data.get(
            "class_group",
            session.class_group,
        )

        if new_class_group.teacher.user_id != user.id:
            raise PermissionDenied(
                "Você não pode mover a aula "
                "para a turma de outro professor."
            )

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            instance.delete()
            return

        if (
            user.role != User.Role.TEACHER
            or instance.class_group.teacher.user_id != user.id
        ):
            raise PermissionDenied(
                "Você não pode excluir esta aula."
            )

        instance.delete()


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = AttendanceRecord.objects.select_related(
            "session",
            "session__class_group",
            "session__class_group__subject",
            "session__class_group__teacher",
            "session__class_group__teacher__user",
            "student",
            "student__user",
        )

        if user.role == User.Role.ADMIN:
            return queryset

        if user.role == User.Role.TEACHER:
            return queryset.filter(
                session__class_group__teacher__user=user,
            )

        if user.role == User.Role.STUDENT:
            return queryset.filter(
                student__user=user,
            )

        return queryset.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            serializer.save()
            return

        if user.role != User.Role.TEACHER:
            raise PermissionDenied(
                "Apenas professores e administradores "
                "podem registrar frequência."
            )

        session = serializer.validated_data["session"]

        if session.class_group.teacher.user_id != user.id:
            raise PermissionDenied(
                "Você só pode registrar frequência "
                "nas suas próprias turmas."
            )

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        attendance = self.get_object()

        if user.role == User.Role.ADMIN:
            serializer.save()
            return

        if (
            user.role != User.Role.TEACHER
            or attendance.session.class_group.teacher.user_id != user.id
        ):
            raise PermissionDenied(
                "Você não pode alterar este "
                "registro de frequência."
            )

        new_session = serializer.validated_data.get(
            "session",
            attendance.session,
        )

        if new_session.class_group.teacher.user_id != user.id:
            raise PermissionDenied(
                "Você não pode mover a frequência "
                "para uma aula de outro professor."
            )

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            instance.delete()
            return

        if (
            user.role != User.Role.TEACHER
            or instance.session.class_group.teacher.user_id != user.id
        ):
            raise PermissionDenied(
                "Você não pode excluir este "
                "registro de frequência."
            )

        instance.delete()