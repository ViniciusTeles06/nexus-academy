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
from attendance.models import (
    AttendanceRecord,
    ClassSession,
)


class AttendanceAPITests(APITestCase):
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
            email="admin@attendance-api.test",
            password="TestPassword123!",
            first_name="Admin",
            last_name="Nexus",
            role=User.Role.ADMIN,
        )

        # PROFESSOR 1
        self.teacher_user = User.objects.create_user(
            email="teacher@attendance-api.test",
            password="TestPassword123!",
            first_name="Professor",
            last_name="Um",
            role=User.Role.TEACHER,
        )

        self.teacher = TeacherProfile.objects.create(
            user=self.teacher_user,
            employee_number="ATT-API-PROF-001",
            specialization="Engenharia de Software",
        )

        # PROFESSOR 2
        self.other_teacher_user = User.objects.create_user(
            email="teacher2@attendance-api.test",
            password="TestPassword123!",
            first_name="Professor",
            last_name="Dois",
            role=User.Role.TEACHER,
        )

        self.other_teacher = TeacherProfile.objects.create(
            user=self.other_teacher_user,
            employee_number="ATT-API-PROF-002",
            specialization="Banco de Dados",
        )

        # ALUNO 1
        self.student_user = User.objects.create_user(
            email="student@attendance-api.test",
            password="TestPassword123!",
            first_name="Aluno",
            last_name="Um",
            role=User.Role.STUDENT,
        )

        self.student = StudentProfile.objects.create(
            user=self.student_user,
            course=self.course,
            registration_number="ATT-API-20260001",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        # ALUNO 2
        self.other_student_user = User.objects.create_user(
            email="student2@attendance-api.test",
            password="TestPassword123!",
            first_name="Aluno",
            last_name="Dois",
            role=User.Role.STUDENT,
        )

        self.other_student = StudentProfile.objects.create(
            user=self.other_student_user,
            course=self.course,
            registration_number="ATT-API-20260002",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        # TURMA PROFESSOR 1
        self.class_group = ClassGroup.objects.create(
            subject=self.subject,
            academic_period=self.period,
            teacher=self.teacher,
            code="CC3A",
            max_students=40,
        )

        # TURMA PROFESSOR 2
        self.other_class_group = ClassGroup.objects.create(
            subject=self.subject,
            academic_period=self.period,
            teacher=self.other_teacher,
            code="CC3B",
            max_students=40,
        )

        # MATRÍCULAS
        Enrollment.objects.create(
            student=self.student,
            class_group=self.class_group,
            status=Enrollment.Status.ACTIVE,
        )

        Enrollment.objects.create(
            student=self.other_student,
            class_group=self.other_class_group,
            status=Enrollment.Status.ACTIVE,
        )

        # AULA PROFESSOR 1
        self.session = ClassSession.objects.create(
            class_group=self.class_group,
            date=date(2026, 9, 1),
            topic="Introdução à Engenharia de Software",
            duration_minutes=100,
        )

        self.second_session = ClassSession.objects.create(
            class_group=self.class_group,
            date=date(2026, 9, 8),
            topic="Modelos de processo",
            duration_minutes=100,
        )

        # AULA PROFESSOR 2
        self.other_session = ClassSession.objects.create(
            class_group=self.other_class_group,
            date=date(2026, 9, 2),
            topic="Introdução a Banco de Dados",
            duration_minutes=100,
        )

        # AULA CANCELADA
        self.cancelled_session = ClassSession.objects.create(
            class_group=self.class_group,
            date=date(2026, 9, 15),
            topic="Aula cancelada",
            duration_minutes=100,
            is_cancelled=True,
        )

        # FREQUÊNCIAS
        self.attendance = AttendanceRecord.objects.create(
            session=self.session,
            student=self.student,
            status=AttendanceRecord.Status.PRESENT,
        )

        self.other_attendance = AttendanceRecord.objects.create(
            session=self.other_session,
            student=self.other_student,
            status=AttendanceRecord.Status.ABSENT,
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_unauthenticated_user_cannot_access_sessions(self):
        response = self.client.get(
            "/api/v1/attendance/sessions/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_admin_sees_all_sessions(self):
        self.authenticate(self.admin)

        response = self.client.get(
            "/api/v1/attendance/sessions/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            4,
        )

    def test_teacher_sees_only_own_sessions(self):
        self.authenticate(self.teacher_user)

        response = self.client.get(
            "/api/v1/attendance/sessions/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            3,
        )

        codes = {
            item["class_code"]
            for item in response.data
        }

        self.assertEqual(
            codes,
            {"CC3A"},
        )

    def test_student_sees_only_enrolled_class_sessions(self):
        self.authenticate(self.student_user)

        response = self.client.get(
            "/api/v1/attendance/sessions/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            3,
        )

        codes = {
            item["class_code"]
            for item in response.data
        }

        self.assertEqual(
            codes,
            {"CC3A"},
        )

    def test_teacher_can_create_session_in_own_class(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/attendance/sessions/",
            {
                "class_group": str(self.class_group.id),
                "date": "2026-09-22",
                "topic": "Arquitetura de software",
                "description": "Introdução à arquitetura.",
                "duration_minutes": 100,
                "is_cancelled": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            ClassSession.objects.filter(
                topic="Arquitetura de software"
            ).exists()
        )

    def test_teacher_cannot_create_session_in_other_class(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/attendance/sessions/",
            {
                "class_group": str(
                    self.other_class_group.id
                ),
                "date": "2026-09-23",
                "topic": "Aula proibida",
                "duration_minutes": 100,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_student_cannot_create_session(self):
        self.authenticate(self.student_user)

        response = self.client.post(
            "/api/v1/attendance/sessions/",
            {
                "class_group": str(self.class_group.id),
                "date": "2026-09-24",
                "topic": "Aula criada por aluno",
                "duration_minutes": 100,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_admin_sees_all_attendance_records(self):
        self.authenticate(self.admin)

        response = self.client.get(
            "/api/v1/attendance/records/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_teacher_sees_only_records_from_own_classes(self):
        self.authenticate(self.teacher_user)

        response = self.client.get(
            "/api/v1/attendance/records/"
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
            "ATT-API-20260001",
        )

    def test_student_sees_only_own_attendance(self):
        self.authenticate(self.student_user)

        response = self.client.get(
            "/api/v1/attendance/records/"
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
            "ATT-API-20260001",
        )

    def test_teacher_can_create_attendance_in_own_class(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/attendance/records/",
            {
                "session": str(self.second_session.id),
                "student": str(self.student.id),
                "status": AttendanceRecord.Status.ABSENT,
                "notes": "Aluno ausente.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            AttendanceRecord.objects.filter(
                session=self.second_session,
                student=self.student,
                status=AttendanceRecord.Status.ABSENT,
            ).exists()
        )

    def test_other_teacher_cannot_create_attendance(self):
        self.authenticate(self.other_teacher_user)

        response = self.client.post(
            "/api/v1/attendance/records/",
            {
                "session": str(self.second_session.id),
                "student": str(self.student.id),
                "status": AttendanceRecord.Status.PRESENT,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_student_cannot_create_attendance(self):
        self.authenticate(self.student_user)

        response = self.client.post(
            "/api/v1/attendance/records/",
            {
                "session": str(self.second_session.id),
                "student": str(self.student.id),
                "status": AttendanceRecord.Status.PRESENT,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_cannot_register_attendance_on_cancelled_session(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/attendance/records/",
            {
                "session": str(
                    self.cancelled_session.id
                ),
                "student": str(self.student.id),
                "status": AttendanceRecord.Status.PRESENT,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "session",
            response.data,
        )

    def test_student_from_other_class_cannot_receive_attendance(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/attendance/records/",
            {
                "session": str(self.second_session.id),
                "student": str(self.other_student.id),
                "status": AttendanceRecord.Status.PRESENT,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "student",
            response.data,
        )