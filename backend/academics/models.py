import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(max_length=150)

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    duration_semesters = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

        constraints = [
            models.CheckConstraint(
                condition=Q(duration_semesters__gt=0),
                name="course_duration_semesters_gt_0",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class AcademicPeriod(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=50,
        unique=True,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-start_date",)

        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__gt=F("start_date")),
                name="academic_period_end_after_start",
            ),
        ]

    def __str__(self):
        return self.name


class Subject(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="subjects",
    )

    name = models.CharField(max_length=150)

    code = models.CharField(
        max_length=30,
        unique=True,
    )

    workload_hours = models.PositiveSmallIntegerField()

    semester = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = (
            "semester",
            "name",
        )

        constraints = [
            models.CheckConstraint(
                condition=Q(workload_hours__gt=0),
                name="subject_workload_gt_0",
            ),
            models.CheckConstraint(
                condition=Q(semester__gt=0),
                name="subject_semester_gt_0",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class StudentProfile(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Ativo"
        INACTIVE = "INACTIVE", "Inativo"
        GRADUATED = "GRADUATED", "Formado"
        SUSPENDED = "SUSPENDED", "Trancado"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="students",
    )

    registration_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )

    admission_date = models.DateField()

    current_semester = models.PositiveSmallIntegerField(
        default=1,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )

    class Meta:
        ordering = ("registration_number",)

        constraints = [
            models.CheckConstraint(
                condition=Q(current_semester__gt=0),
                name="student_current_semester_gt_0",
            ),
        ]

    def clean(self):
        super().clean()

        if self.user_id and self.user.role != "STUDENT":
            raise ValidationError(
                {
                    "user": (
                        "Somente usuários com perfil STUDENT "
                        "podem possuir perfil de aluno."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.registration_number} - "
            f"{self.user.get_full_name()}"
        )


class TeacherProfile(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )

    employee_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )

    specialization = models.CharField(
        max_length=150,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("employee_number",)

    def clean(self):
        super().clean()

        if self.user_id and self.user.role != "TEACHER":
            raise ValidationError(
                {
                    "user": (
                        "Somente usuários com perfil TEACHER "
                        "podem possuir perfil de professor."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.employee_number} - "
            f"{self.user.get_full_name()}"
        )


class ClassGroup(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="classes",
    )

    academic_period = models.ForeignKey(
        AcademicPeriod,
        on_delete=models.PROTECT,
        related_name="classes",
    )

    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.PROTECT,
        related_name="classes",
    )

    code = models.CharField(max_length=30)

    max_students = models.PositiveSmallIntegerField(
        default=40,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = (
            "academic_period",
            "subject",
            "code",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "subject",
                    "academic_period",
                    "code",
                ],
                name="unique_class_per_subject_period_code",
            ),
            models.CheckConstraint(
                condition=Q(max_students__gt=0),
                name="class_max_students_gt_0",
            ),
        ]

    def __str__(self):
        return (
            f"{self.subject.code} - "
            f"{self.code} - "
            f"{self.academic_period.name}"
        )


class Enrollment(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Matriculado"
        CANCELLED = "CANCELLED", "Cancelado"
        COMPLETED = "COMPLETED", "Concluído"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-enrolled_at",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "class_group",
                ],
                name="unique_student_class_enrollment",
            ),
        ]

    def clean(self):
        super().clean()

        if (
            self.student_id
            and self.class_group_id
            and self.student.course_id
            != self.class_group.subject.course_id
        ):
            raise ValidationError(
                {
                    "class_group": (
                        "O aluno não pertence ao curso "
                        "desta disciplina."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.student.registration_number} - "
            f"{self.class_group}"
        )