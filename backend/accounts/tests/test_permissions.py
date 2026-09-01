from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import User
from accounts.permissions import (
    IsAdmin,
    IsStudent,
    IsStudentOrAdmin,
    IsTeacher,
    IsTeacherOrAdmin,
)


class RolePermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.student = User.objects.create_user(
            email="student@nexus.test",
            password="TestPassword123!",
            first_name="Student",
            last_name="Test",
            role=User.Role.STUDENT,
        )

        self.teacher = User.objects.create_user(
            email="teacher@nexus.test",
            password="TestPassword123!",
            first_name="Teacher",
            last_name="Test",
            role=User.Role.TEACHER,
        )

        self.admin = User.objects.create_user(
            email="admin@nexus.test",
            password="TestPassword123!",
            first_name="Admin",
            last_name="Test",
            role=User.Role.ADMIN,
        )

    def make_request(self, user):
        django_request = self.factory.get("/")
        force_authenticate(django_request, user=user)

        return Request(django_request)

    def test_student_permission_accepts_student(self):
        request = self.make_request(self.student)

        self.assertTrue(
            IsStudent().has_permission(request, None)
        )

    def test_student_permission_rejects_teacher(self):
        request = self.make_request(self.teacher)

        self.assertFalse(
            IsStudent().has_permission(request, None)
        )

    def test_teacher_permission_accepts_teacher(self):
        request = self.make_request(self.teacher)

        self.assertTrue(
            IsTeacher().has_permission(request, None)
        )

    def test_teacher_permission_rejects_student(self):
        request = self.make_request(self.student)

        self.assertFalse(
            IsTeacher().has_permission(request, None)
        )

    def test_admin_permission_accepts_admin(self):
        request = self.make_request(self.admin)

        self.assertTrue(
            IsAdmin().has_permission(request, None)
        )

    def test_admin_permission_rejects_student(self):
        request = self.make_request(self.student)

        self.assertFalse(
            IsAdmin().has_permission(request, None)
        )

    def test_teacher_or_admin_accepts_teacher(self):
        request = self.make_request(self.teacher)

        self.assertTrue(
            IsTeacherOrAdmin().has_permission(request, None)
        )

    def test_teacher_or_admin_accepts_admin(self):
        request = self.make_request(self.admin)

        self.assertTrue(
            IsTeacherOrAdmin().has_permission(request, None)
        )

    def test_teacher_or_admin_rejects_student(self):
        request = self.make_request(self.student)

        self.assertFalse(
            IsTeacherOrAdmin().has_permission(request, None)
        )

    def test_student_or_admin_accepts_student(self):
        request = self.make_request(self.student)

        self.assertTrue(
            IsStudentOrAdmin().has_permission(request, None)
        )

    def test_student_or_admin_accepts_admin(self):
        request = self.make_request(self.admin)

        self.assertTrue(
            IsStudentOrAdmin().has_permission(request, None)
        )

    def test_student_or_admin_rejects_teacher(self):
        request = self.make_request(self.teacher)

        self.assertFalse(
            IsStudentOrAdmin().has_permission(request, None)
        )