import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from academics.models import (
    ClassGroup,
    Enrollment,
    StudentProfile,
)


class ClassSession(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.PROTECT,
        related_name="sessions",
    )

    date = models.DateField(
        db_index=True,
    )

    topic = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    duration_minutes = models.PositiveSmallIntegerField(
        default=100,
    )

    is_cancelled = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = (
            "-date",
            "class_group",
        )

        constraints = [
            models.CheckConstraint(
                condition=Q(duration_minutes__gt=0),
                name="class_session_duration_gt_0",
            ),
            models.UniqueConstraint(
                fields=[
                    "class_group",
                    "date",
                    "topic",
                ],
                name="unique_session_class_date_topic",
            ),
        ]

    def __str__(self):
        return (
            f"{self.class_group} - "
            f"{self.date} - "
            f"{self.topic}"
        )


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Presente"
        ABSENT = "ABSENT", "Falta"
        EXCUSED = "EXCUSED", "Falta justificada"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    session = models.ForeignKey(
        ClassSession,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PRESENT,
        db_index=True,
    )

    notes = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = (
            "session",
            "student",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "session",
                    "student",
                ],
                name="unique_attendance_student_session",
            ),
        ]

    def clean(self):
        super().clean()

        if not self.session_id or not self.student_id:
            return

        class_group = self.session.class_group

        if self.session.is_cancelled:
            raise ValidationError(
                {
                    "session": (
                        "Não é possível registrar frequência "
                        "em uma aula cancelada."
                    )
                }
            )

        is_enrolled = Enrollment.objects.filter(
            student=self.student,
            class_group=class_group,
            status=Enrollment.Status.ACTIVE,
        ).exists()

        if not is_enrolled:
            raise ValidationError(
                {
                    "student": (
                        "O aluno precisa estar matriculado "
                        "na turma desta aula."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.student.registration_number} - "
            f"{self.session.date} - "
            f"{self.get_status_display()}"
        )