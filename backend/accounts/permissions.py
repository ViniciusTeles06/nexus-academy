from rest_framework.permissions import BasePermission

from .models import User


class IsStudent(BasePermission):
    message = "Acesso permitido apenas para alunos."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.STUDENT
        )


class IsTeacher(BasePermission):
    message = "Acesso permitido apenas para professores."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.TEACHER
        )


class IsAdmin(BasePermission):
    message = "Acesso permitido apenas para administradores."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.role == User.Role.ADMIN
                or request.user.is_superuser
            )
        )


class IsTeacherOrAdmin(BasePermission):
    message = "Acesso permitido apenas para professores ou administradores."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return (
            request.user.role in {
                User.Role.TEACHER,
                User.Role.ADMIN,
            }
            or request.user.is_superuser
        )


class IsStudentOrAdmin(BasePermission):
    message = "Acesso permitido apenas para alunos ou administradores."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return (
            request.user.role in {
                User.Role.STUDENT,
                User.Role.ADMIN,
            }
            or request.user.is_superuser
        )