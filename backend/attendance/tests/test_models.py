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
from attendance.models import (
    AttendanceRecord,
    ClassSession,
)


class AttendanceModelTests(TestCase):
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
            email="teacher@attendance.test",
            password="TestPassword123!",
            first_name="Professor",
            last_name="Teste",
            role=User.Role.TEACHER,
        )

        self.teacher = TeacherProfile.objects.create(
            user=self.teacher_user,
            employee_number="ATT-PROF-001",
            specialization="Engenharia de Software",
        )

        self.student_user = User.objects.create_user(
            email="student@attendance.test",
            password="TestPassword123!",
            first_name="Aluno",
            last_name="Teste",
            role=User.Role.STUDENT,
        )

        self.student = StudentProfile.objects.create(
            user=self.student_user,
            course=self.course,
            registration_number="ATT-20260001",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        self.other_student_user = User.objects.create_user(
            email="other.student@attendance.test",
            password="TestPassword123!",
            first_name="Outro",
            last_name="Aluno",
            role=User.Role.STUDENT,
        )

        self.other_student = StudentProfile.objects.create(
            user=self.other_student_user,
            course=self.course,
            registration_number="ATT-20260002",
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

        self.session = ClassSession.objects.create(
            class_group=self.class_group,
            date=date(2026, 9, 1),
            topic="Introdução à Engenharia de Software",
            description="Conceitos iniciais da disciplina.",
            duration_minutes=100,
        )

    def test_valid_class_session(self):
        self.session.full_clean()

        self.assertEqual(
            self.session.duration_minutes,
            100,
        )

    def test_class_session_duration_must_be_greater_than_zero(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ClassSession.objects.create(
                    class_group=self.class_group,
                    date=date(2026, 9, 2),
                    topic="Aula inválida",
                    duration_minutes=0,
                )

    def test_duplicate_class_session_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ClassSession.objects.create(
                    class_group=self.class_group,
                    date=date(2026, 9, 1),
                    topic="Introdução à Engenharia de Software",
                    duration_minutes=100,
                )

    def test_valid_attendance_record(self):
        attendance = AttendanceRecord(
            session=self.session,
            student=self.student,
            status=AttendanceRecord.Status.PRESENT,
        )

        attendance.full_clean()
        attendance.save()

        self.assertEqual(
            attendance.status,
            AttendanceRecord.Status.PRESENT,
        )

    def test_absent_status_is_valid(self):
        attendance = AttendanceRecord(
            session=self.session,
            student=self.student,
            status=AttendanceRecord.Status.ABSENT,
        )

        attendance.full_clean()

    def test_excused_status_is_valid(self):
        attendance = AttendanceRecord(
            session=self.session,
            student=self.student,
            status=AttendanceRecord.Status.EXCUSED,
        )

        attendance.full_clean()

    def test_student_must_be_enrolled_in_class(self):
        attendance = AttendanceRecord(
            session=self.session,
            student=self.other_student,
            status=AttendanceRecord.Status.PRESENT,
        )

        with self.assertRaises(ValidationError):
            attendance.full_clean()

    def test_cancelled_enrollment_cannot_receive_attendance(self):
        self.enrollment.status = Enrollment.Status.CANCELLED
        self.enrollment.save()

        attendance = AttendanceRecord(
            session=self.session,
            student=self.student,
            status=AttendanceRecord.Status.PRESENT,
        )

        with self.assertRaises(ValidationError):
            attendance.full_clean()

    def test_duplicate_attendance_record_is_rejected(self):
        AttendanceRecord.objects.create(
            session=self.session,
            student=self.student,
            status=AttendanceRecord.Status.PRESENT,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                AttendanceRecord.objects.create(
                    session=self.session,
                    student=self.student,
                    status=AttendanceRecord.Status.ABSENT,
                )

    def test_cancelled_session_can_be_saved(self):
        session = ClassSession.objects.create(
            class_group=self.class_group,
            date=date(2026, 9, 3),
            topic="Aula cancelada",
            duration_minutes=100,
            is_cancelled=True,
        )

        self.assertTrue(session.is_cancelled)