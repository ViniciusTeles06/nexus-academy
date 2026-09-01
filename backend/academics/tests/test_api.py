from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from academics.models import (
    AcademicPeriod,
    ClassGroup,
    Course,
    Enrollment,
    StudentProfile,
    Subject,
    TeacherProfile,
)


class AcademicAPITests(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name="Ciência da Computação",
            code="CC",
            duration_semesters=8,
        )

        self.period = AcademicPeriod.objects.create(
            name="2026.2",
            start_date=date(2026, 8, 1),
            end_date=date(2026, 12, 20),
        )

        self.subject = Subject.objects.create(
            course=self.course,
            name="Engenharia de Software",
            code="ESW101",
            workload_hours=80,
            semester=3,
        )

        # ADMIN
        self.admin = User.objects.create_user(
            email="admin@nexus.test",
            password="TestPassword123!",
            first_name="Admin",
            last_name="Nexus",
            role=User.Role.ADMIN,
        )

        # PROFESSOR 1
        self.teacher_user = User.objects.create_user(
            email="teacher@nexus.test",
            password="TestPassword123!",
            first_name="Professor",
            last_name="Um",
            role=User.Role.TEACHER,
        )

        self.teacher = TeacherProfile.objects.create(
            user=self.teacher_user,
            employee_number="PROF001",
            specialization="Engenharia de Software",
        )

        # PROFESSOR 2
        self.other_teacher_user = User.objects.create_user(
            email="teacher2@nexus.test",
            password="TestPassword123!",
            first_name="Professor",
            last_name="Dois",
            role=User.Role.TEACHER,
        )

        self.other_teacher = TeacherProfile.objects.create(
            user=self.other_teacher_user,
            employee_number="PROF002",
            specialization="Banco de Dados",
        )

        # ALUNO 1
        self.student_user = User.objects.create_user(
            email="student@nexus.test",
            password="TestPassword123!",
            first_name="Aluno",
            last_name="Um",
            role=User.Role.STUDENT,
        )

        self.student = StudentProfile.objects.create(
            user=self.student_user,
            course=self.course,
            registration_number="20260001",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        # ALUNO 2
        self.other_student_user = User.objects.create_user(
            email="student2@nexus.test",
            password="TestPassword123!",
            first_name="Aluno",
            last_name="Dois",
            role=User.Role.STUDENT,
        )

        self.other_student = StudentProfile.objects.create(
            user=self.other_student_user,
            course=self.course,
            registration_number="20260002",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        # TURMA DO PROFESSOR 1
        self.class_group = ClassGroup.objects.create(
            subject=self.subject,
            academic_period=self.period,
            teacher=self.teacher,
            code="CC3A",
            max_students=40,
        )

        # TURMA DO PROFESSOR 2
        self.other_class_group = ClassGroup.objects.create(
            subject=self.subject,
            academic_period=self.period,
            teacher=self.other_teacher,
            code="CC3B",
            max_students=40,
        )

        # ALUNO 1 → CC3A
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            class_group=self.class_group,
        )

        # ALUNO 2 → CC3B
        self.other_enrollment = Enrollment.objects.create(
            student=self.other_student,
            class_group=self.other_class_group,
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_unauthenticated_user_cannot_access_courses(self):
        response = self.client.get(
            "/api/v1/academics/courses/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_admin_can_create_course(self):
        self.authenticate(self.admin)

        response = self.client.post(
            "/api/v1/academics/courses/",
            {
                "name": "Sistemas de Informação",
                "code": "SI",
                "duration_semesters": 8,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Course.objects.filter(code="SI").exists()
        )

    def test_student_cannot_create_course(self):
        self.authenticate(self.student_user)

        response = self.client.post(
            "/api/v1/academics/courses/",
            {
                "name": "Curso proibido",
                "code": "BLOCKED-STUDENT",
                "duration_semesters": 8,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_teacher_cannot_create_course(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/academics/courses/",
            {
                "name": "Curso proibido",
                "code": "BLOCKED-TEACHER",
                "duration_semesters": 8,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_admin_sees_all_classes(self):
        self.authenticate(self.admin)

        response = self.client.get(
            "/api/v1/academics/classes/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_teacher_sees_only_own_classes(self):
        self.authenticate(self.teacher_user)

        response = self.client.get(
            "/api/v1/academics/classes/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["code"],
            "CC3A",
        )

    def test_student_sees_only_enrolled_classes(self):
        self.authenticate(self.student_user)

        response = self.client.get(
            "/api/v1/academics/classes/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["code"],
            "CC3A",
        )

    def test_admin_sees_all_enrollments(self):
        self.authenticate(self.admin)

        response = self.client.get(
            "/api/v1/academics/enrollments/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_teacher_sees_only_enrollments_from_own_classes(self):
        self.authenticate(self.teacher_user)

        response = self.client.get(
            "/api/v1/academics/enrollments/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["registration_number"],
            "20260001",
        )

    def test_student_sees_only_own_enrollments(self):
        self.authenticate(self.student_user)

        response = self.client.get(
            "/api/v1/academics/enrollments/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["registration_number"],
            "20260001",
        )