from datetime import date
from decimal import Decimal

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
from grading.models import Assessment, Grade


class GradingAPITests(APITestCase):
    def setUp(self):
        # CURSO
        self.course = Course.objects.create(
            name="Ciência da Computação",
            code="CC",
            duration_semesters=8,
        )

        # PERÍODO
        self.period = AcademicPeriod.objects.create(
            name="2026.2",
            start_date=date(2026, 8, 1),
            end_date=date(2026, 12, 20),
        )

        # DISCIPLINA
        self.subject = Subject.objects.create(
            course=self.course,
            name="Engenharia de Software",
            code="ESW101",
            workload_hours=80,
            semester=3,
        )

        # =========================
        # ADMIN
        # =========================

        self.admin = User.objects.create_user(
            email="admin@grading-api.test",
            password="TestPassword123!",
            first_name="Admin",
            last_name="Nexus",
            role=User.Role.ADMIN,
        )

        # =========================
        # PROFESSOR 1
        # =========================

        self.teacher_user = User.objects.create_user(
            email="teacher@grading-api.test",
            password="TestPassword123!",
            first_name="Professor",
            last_name="Um",
            role=User.Role.TEACHER,
        )

        self.teacher = TeacherProfile.objects.create(
            user=self.teacher_user,
            employee_number="API-PROF-001",
            specialization="Engenharia de Software",
        )

        # =========================
        # PROFESSOR 2
        # =========================

        self.other_teacher_user = User.objects.create_user(
            email="teacher2@grading-api.test",
            password="TestPassword123!",
            first_name="Professor",
            last_name="Dois",
            role=User.Role.TEACHER,
        )

        self.other_teacher = TeacherProfile.objects.create(
            user=self.other_teacher_user,
            employee_number="API-PROF-002",
            specialization="Banco de Dados",
        )

        # =========================
        # ALUNO 1
        # =========================

        self.student_user = User.objects.create_user(
            email="student@grading-api.test",
            password="TestPassword123!",
            first_name="Aluno",
            last_name="Um",
            role=User.Role.STUDENT,
        )

        self.student = StudentProfile.objects.create(
            user=self.student_user,
            course=self.course,
            registration_number="API-20260001",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        # =========================
        # ALUNO 2
        # =========================

        self.other_student_user = User.objects.create_user(
            email="student2@grading-api.test",
            password="TestPassword123!",
            first_name="Aluno",
            last_name="Dois",
            role=User.Role.STUDENT,
        )

        self.other_student = StudentProfile.objects.create(
            user=self.other_student_user,
            course=self.course,
            registration_number="API-20260002",
            admission_date=date(2026, 2, 1),
            current_semester=3,
        )

        # =========================
        # TURMA PROFESSOR 1
        # =========================

        self.class_group = ClassGroup.objects.create(
            subject=self.subject,
            academic_period=self.period,
            teacher=self.teacher,
            code="CC3A",
            max_students=40,
        )

        # =========================
        # TURMA PROFESSOR 2
        # =========================

        self.other_class_group = ClassGroup.objects.create(
            subject=self.subject,
            academic_period=self.period,
            teacher=self.other_teacher,
            code="CC3B",
            max_students=40,
        )

        # =========================
        # MATRÍCULAS
        # =========================

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

        # =========================
        # AVALIAÇÃO PUBLICADA
        # =========================

        self.published_assessment = Assessment.objects.create(
            class_group=self.class_group,
            title="Prova publicada",
            assessment_type=Assessment.Type.EXAM,
            max_score=Decimal("10.00"),
            weight=Decimal("2.00"),
            assessment_date=date(2026, 9, 15),
            is_published=True,
        )

        # =========================
        # AVALIAÇÃO NÃO PUBLICADA
        # =========================

        self.hidden_assessment = Assessment.objects.create(
            class_group=self.class_group,
            title="Prova não publicada",
            assessment_type=Assessment.Type.EXAM,
            max_score=Decimal("10.00"),
            weight=Decimal("1.00"),
            assessment_date=date(2026, 10, 15),
            is_published=False,
        )

        # =========================
        # OUTRA AVALIAÇÃO PROF. 1
        # =========================

        self.second_assessment = Assessment.objects.create(
            class_group=self.class_group,
            title="Trabalho 1",
            assessment_type=Assessment.Type.ASSIGNMENT,
            max_score=Decimal("10.00"),
            weight=Decimal("1.00"),
            assessment_date=date(2026, 9, 25),
            is_published=True,
        )

        # =========================
        # AVALIAÇÃO PROFESSOR 2
        # =========================

        self.other_assessment = Assessment.objects.create(
            class_group=self.other_class_group,
            title="Prova outra turma",
            assessment_type=Assessment.Type.EXAM,
            max_score=Decimal("10.00"),
            weight=Decimal("1.00"),
            assessment_date=date(2026, 9, 20),
            is_published=True,
        )

        # =========================
        # NOTAS
        # =========================

        self.grade = Grade.objects.create(
            assessment=self.published_assessment,
            student=self.student,
            score=Decimal("8.50"),
        )

        self.hidden_grade = Grade.objects.create(
            assessment=self.hidden_assessment,
            student=self.student,
            score=Decimal("7.00"),
        )

        self.other_grade = Grade.objects.create(
            assessment=self.other_assessment,
            student=self.other_student,
            score=Decimal("9.00"),
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # ==================================================
    # AUTENTICAÇÃO
    # ==================================================

    def test_unauthenticated_user_cannot_access_assessments(self):
        response = self.client.get(
            "/api/v1/grading/assessments/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    # ==================================================
    # ADMIN
    # ==================================================

    def test_admin_sees_all_assessments(self):
        self.authenticate(self.admin)

        response = self.client.get(
            "/api/v1/grading/assessments/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            4,
        )

    def test_admin_sees_all_grades(self):
        self.authenticate(self.admin)

        response = self.client.get(
            "/api/v1/grading/grades/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            3,
        )

    # ==================================================
    # PROFESSOR
    # ==================================================

    def test_teacher_sees_only_own_assessments(self):
        self.authenticate(self.teacher_user)

        response = self.client.get(
            "/api/v1/grading/assessments/"
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

    def test_teacher_can_create_assessment_in_own_class(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/grading/assessments/",
            {
                "class_group": str(
                    self.class_group.id
                ),
                "title": "Projeto final",
                "description": (
                    "Projeto final da disciplina."
                ),
                "assessment_type": (
                    Assessment.Type.PROJECT
                ),
                "max_score": "10.00",
                "weight": "3.00",
                "assessment_date": "2026-11-10",
                "is_published": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Assessment.objects.filter(
                title="Projeto final",
                class_group=self.class_group,
            ).exists()
        )

    def test_teacher_cannot_create_assessment_in_other_class(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/grading/assessments/",
            {
                "class_group": str(
                    self.other_class_group.id
                ),
                "title": "Avaliação proibida",
                "assessment_type": (
                    Assessment.Type.EXAM
                ),
                "max_score": "10.00",
                "weight": "1.00",
                "assessment_date": "2026-11-15",
                "is_published": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_teacher_sees_only_grades_from_own_classes(self):
        self.authenticate(self.teacher_user)

        response = self.client.get(
            "/api/v1/grading/grades/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

        for grade in response.data:
            self.assertEqual(
                grade["registration_number"],
                "API-20260001",
            )

    def test_teacher_can_create_grade_in_own_class(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/grading/grades/",
            {
                "assessment": str(
                    self.second_assessment.id
                ),
                "student": str(
                    self.student.id
                ),
                "score": "9.25",
                "feedback": "Ótimo trabalho.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Grade.objects.filter(
                assessment=self.second_assessment,
                student=self.student,
            ).exists()
        )

    def test_other_teacher_cannot_create_grade(self):
        self.authenticate(
            self.other_teacher_user
        )

        response = self.client.post(
            "/api/v1/grading/grades/",
            {
                "assessment": str(
                    self.second_assessment.id
                ),
                "student": str(
                    self.student.id
                ),
                "score": "8.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ==================================================
    # ALUNO
    # ==================================================

    def test_student_sees_only_published_assessments(self):
        self.authenticate(self.student_user)

        response = self.client.get(
            "/api/v1/grading/assessments/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        titles = {
            item["title"]
            for item in response.data
        }

        self.assertIn(
            "Prova publicada",
            titles,
        )

        self.assertIn(
            "Trabalho 1",
            titles,
        )

        self.assertNotIn(
            "Prova não publicada",
            titles,
        )

        self.assertNotIn(
            "Prova outra turma",
            titles,
        )

    def test_student_cannot_create_assessment(self):
        self.authenticate(self.student_user)

        response = self.client.post(
            "/api/v1/grading/assessments/",
            {
                "class_group": str(
                    self.class_group.id
                ),
                "title": "Avaliação criada por aluno",
                "assessment_type": (
                    Assessment.Type.EXAM
                ),
                "max_score": "10.00",
                "weight": "1.00",
                "assessment_date": "2026-11-20",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_student_sees_only_own_published_grades(self):
        self.authenticate(self.student_user)

        response = self.client.get(
            "/api/v1/grading/grades/"
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
            response.data[0][
                "registration_number"
            ],
            "API-20260001",
        )

        self.assertEqual(
            response.data[0][
                "assessment_title"
            ],
            "Prova publicada",
        )

    def test_student_cannot_create_grade(self):
        self.authenticate(self.student_user)

        response = self.client.post(
            "/api/v1/grading/grades/",
            {
                "assessment": str(
                    self.second_assessment.id
                ),
                "student": str(
                    self.student.id
                ),
                "score": "10.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ==================================================
    # VALIDAÇÃO DE NOTA
    # ==================================================

    def test_grade_above_max_score_is_rejected(self):
        self.authenticate(self.teacher_user)

        response = self.client.post(
            "/api/v1/grading/grades/",
            {
                "assessment": str(
                    self.second_assessment.id
                ),
                "student": str(
                    self.student.id
                ),
                "score": "11.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "score",
            response.data,
        )