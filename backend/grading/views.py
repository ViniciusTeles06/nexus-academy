from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from accounts.models import User

from .models import Assessment, Grade
from .serializers import AssessmentSerializer, GradeSerializer


class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Assessment.objects.select_related(
            "class_group",
            "class_group__subject",
            "class_group__teacher",
            "class_group__teacher__user",
            "class_group__academic_period",
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
                is_published=True,
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
                "podem criar avaliações."
            )

        class_group = serializer.validated_data["class_group"]

        if class_group.teacher.user_id != user.id:
            raise PermissionDenied(
                "Você só pode criar avaliações "
                "nas suas próprias turmas."
            )

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        assessment = self.get_object()

        if user.role == User.Role.ADMIN:
            serializer.save()
            return

        if (
            user.role != User.Role.TEACHER
            or assessment.class_group.teacher.user_id != user.id
        ):
            raise PermissionDenied(
                "Você não pode alterar esta avaliação."
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
                "Você não pode excluir esta avaliação."
            )

        instance.delete()


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Grade.objects.select_related(
            "assessment",
            "assessment__class_group",
            "assessment__class_group__subject",
            "assessment__class_group__teacher",
            "assessment__class_group__teacher__user",
            "student",
            "student__user",
        )

        if user.role == User.Role.ADMIN:
            return queryset

        if user.role == User.Role.TEACHER:
            return queryset.filter(
                assessment__class_group__teacher__user=user,
            )

        if user.role == User.Role.STUDENT:
            return queryset.filter(
                student__user=user,
                assessment__is_published=True,
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
                "podem lançar notas."
            )

        assessment = serializer.validated_data["assessment"]

        if assessment.class_group.teacher.user_id != user.id:
            raise PermissionDenied(
                "Você só pode lançar notas "
                "nas suas próprias turmas."
            )

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        grade = self.get_object()

        if user.role == User.Role.ADMIN:
            serializer.save()
            return

        if (
            user.role != User.Role.TEACHER
            or grade.assessment.class_group.teacher.user_id != user.id
        ):
            raise PermissionDenied(
                "Você não pode alterar esta nota."
            )

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            instance.delete()
            return

        if (
            user.role != User.Role.TEACHER
            or instance.assessment.class_group.teacher.user_id != user.id
        ):
            raise PermissionDenied(
                "Você não pode excluir esta nota."
            )

        instance.delete()