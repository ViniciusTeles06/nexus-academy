from datetime import date
from decimal import Decimal

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
from grading.models import Assessment, Grade


class GradingModelTests(TestCase):
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

        self.teacher_user = User.objects.create_user(
            email="teacher@grading.test",
            password="TestPassword123!",
            first_name="Professor",
            last_name="Teste",
            role=User.Role.TEACHER,
        )

        self.teacher = TeacherProfile.objects.create(
            user=self.teacher_user,
            employee_number="PROF-GRADING-001",
            specialization="Engenharia de Software",
        )

        self.student_user = User.objects.create_user(
            email="student@grading.test",
            password="TestPassword123!",
            first_name="Aluno",
            last_name="Teste",
            role=User.Role.STUDENT,
        )

        self.student = StudentProfile.objects.create(
            user=self.student_user,
            course=self.course,
            registration_number="GRADING-20260001",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        self.other_student_user = User.objects.create_user(
            email="other.student@grading.test",
            password="TestPassword123!",
            first_name="Outro",
            last_name="Aluno",
            role=User.Role.STUDENT,
        )

        self.other_student = StudentProfile.objects.create(
            user=self.other_student_user,
            course=self.course,
            registration_number="GRADING-20260002",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        self.class_group = ClassGroup.objects.create(
            subject=self.subject,
            academic_period=self.period,
            teacher=self.teacher,
            code="CC3A",
            max_students=40,
        )

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            class_group=self.class_group,
            status=Enrollment.Status.ACTIVE,
        )

        self.assessment = Assessment.objects.create(
            class_group=self.class_group,
            title="Prova 1",
            description="Primeira avaliação da disciplina.",
            assessment_type=Assessment.Type.EXAM,
            max_score=Decimal("10.00"),
            weight=Decimal("2.00"),
            assessment_date=date(2026, 9, 15),
        )

    def test_valid_assessment(self):
        self.assessment.full_clean()

        self.assertEqual(
            self.assessment.max_score,
            Decimal("10.00"),
        )

        self.assertEqual(
            self.assessment.weight,
            Decimal("2.00"),
        )

    def test_assessment_max_score_must_be_greater_than_zero(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Assessment.objects.create(
                    class_group=self.class_group,
                    title="Avaliação inválida",
                    assessment_type=Assessment.Type.EXAM,
                    max_score=Decimal("0.00"),
                    weight=Decimal("1.00"),
                    assessment_date=date(2026, 9, 20),
                )

    def test_assessment_weight_must_be_greater_than_zero(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Assessment.objects.create(
                    class_group=self.class_group,
                    title="Avaliação sem peso",
                    assessment_type=Assessment.Type.ACTIVITY,
                    max_score=Decimal("10.00"),
                    weight=Decimal("0.00"),
                    assessment_date=date(2026, 9, 21),
                )

    def test_duplicate_assessment_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Assessment.objects.create(
                    class_group=self.class_group,
                    title="Prova 1",
                    assessment_type=Assessment.Type.EXAM,
                    max_score=Decimal("10.00"),
                    weight=Decimal("1.00"),
                    assessment_date=date(2026, 9, 15),
                )

    def test_valid_grade(self):
        grade = Grade(
            assessment=self.assessment,
            student=self.student,
            score=Decimal("8.50"),
            feedback="Bom desempenho.",
        )

        grade.full_clean()
        grade.save()

        self.assertEqual(
            grade.score,
            Decimal("8.50"),
        )

    def test_grade_cannot_exceed_max_score(self):
        grade = Grade(
            assessment=self.assessment,
            student=self.student,
            score=Decimal("11.00"),
        )

        with self.assertRaises(ValidationError):
            grade.full_clean()

    def test_negative_grade_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Grade.objects.create(
                    assessment=self.assessment,
                    student=self.student,
                    score=Decimal("-1.00"),
                )

    def test_student_must_be_enrolled_in_class(self):
        grade = Grade(
            assessment=self.assessment,
            student=self.other_student,
            score=Decimal("7.00"),
        )

        with self.assertRaises(ValidationError):
            grade.full_clean()

    def test_duplicate_grade_is_rejected(self):
        Grade.objects.create(
            assessment=self.assessment,
            student=self.student,
            score=Decimal("8.00"),
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Grade.objects.create(
                    assessment=self.assessment,
                    student=self.student,
                    score=Decimal("9.00"),
                )

    def test_cancelled_enrollment_cannot_receive_grade(self):
        self.enrollment.status = Enrollment.Status.CANCELLED
        self.enrollment.save()

        grade = Grade(
            assessment=self.assessment,
            student=self.student,
            score=Decimal("7.00"),
        )

        with self.assertRaises(ValidationError):
            grade.full_clean()