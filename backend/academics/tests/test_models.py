from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

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


class AcademicModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name="Ciência da Computação",
            code="CC",
            duration_semesters=8,
        )

        self.other_course = Course.objects.create(
            name="Administração",
            code="ADM",
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

        self.student_user = User.objects.create_user(
            email="student@nexus.test",
            password="TestPassword123!",
            first_name="Aluno",
            last_name="Teste",
            role=User.Role.STUDENT,
        )

        self.teacher_user = User.objects.create_user(
            email="teacher@nexus.test",
            password="TestPassword123!",
            first_name="Professor",
            last_name="Teste",
            role=User.Role.TEACHER,
        )

        self.admin_user = User.objects.create_user(
            email="admin@nexus.test",
            password="TestPassword123!",
            first_name="Admin",
            last_name="Teste",
            role=User.Role.ADMIN,
        )

        self.student = StudentProfile.objects.create(
            user=self.student_user,
            course=self.course,
            registration_number="20260001",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        self.teacher = TeacherProfile.objects.create(
            user=self.teacher_user,
            employee_number="PROF001",
            specialization="Engenharia de Software",
        )

        self.class_group = ClassGroup.objects.create(
            subject=self.subject,
            academic_period=self.period,
            teacher=self.teacher,
            code="CC3A",
            max_students=40,
        )

    def test_student_profile_accepts_student_user(self):
        self.student.full_clean()

    def test_student_profile_rejects_teacher_user(self):
        profile = StudentProfile(
            user=self.teacher_user,
            course=self.course,
            registration_number="20260002",
            admission_date=date(2026, 2, 1),
        )

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_teacher_profile_accepts_teacher_user(self):
        self.teacher.full_clean()

    def test_teacher_profile_rejects_student_user(self):
        profile = TeacherProfile(
            user=self.student_user,
            employee_number="PROF002",
        )

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_valid_enrollment(self):
        enrollment = Enrollment(
            student=self.student,
            class_group=self.class_group,
        )

        enrollment.full_clean()
        enrollment.save()

        self.assertEqual(
            enrollment.status,
            Enrollment.Status.ACTIVE,
        )

    def test_enrollment_rejects_student_from_other_course(self):
        other_student_user = User.objects.create_user(
            email="other.student@nexus.test",
            password="TestPassword123!",
            first_name="Outro",
            last_name="Aluno",
            role=User.Role.STUDENT,
        )

        other_student = StudentProfile.objects.create(
            user=other_student_user,
            course=self.other_course,
            registration_number="20260003",
            admission_date=date(2026, 2, 1),
        )

        enrollment = Enrollment(
            student=other_student,
            class_group=self.class_group,
        )

        with self.assertRaises(ValidationError):
            enrollment.full_clean()

    def test_duplicate_enrollment_is_rejected(self):
        Enrollment.objects.create(
            student=self.student,
            class_group=self.class_group,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Enrollment.objects.create(
                    student=self.student,
                    class_group=self.class_group,
                )

    def test_invalid_academic_period_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                AcademicPeriod.objects.create(
                    name="2027.1 inválido",
                    start_date=date(2027, 6, 1),
                    end_date=date(2027, 2, 1),
                )

    def test_course_duration_must_be_greater_than_zero(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Course.objects.create(
                    name="Curso inválido",
                    code="INVALID",
                    duration_semesters=0,
                )

    def test_subject_workload_must_be_greater_than_zero(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Subject.objects.create(
                    course=self.course,
                    name="Disciplina inválida",
                    code="INV101",
                    workload_hours=0,
                    semester=1,
                )