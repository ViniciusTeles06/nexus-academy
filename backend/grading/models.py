import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from academics.models import (
    ClassGroup,
    Enrollment,
    StudentProfile,
)


class Assessment(models.Model):
    class Type(models.TextChoices):
        EXAM = "EXAM", "Prova"
        ASSIGNMENT = "ASSIGNMENT", "Trabalho"
        PROJECT = "PROJECT", "Projeto"
        ACTIVITY = "ACTIVITY", "Atividade"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.PROTECT,
        related_name="assessments",
    )

    title = models.CharField(
        max_length=150,
    )

    description = models.TextField(
        blank=True,
    )

    assessment_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.EXAM,
        db_index=True,
    )

    max_score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=10,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1,
    )

    assessment_date = models.DateField()

    is_published = models.BooleanField(
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
            "assessment_date",
            "title",
        )

        constraints = [
            models.CheckConstraint(
                condition=Q(max_score__gt=0),
                name="assessment_max_score_gt_0",
            ),
            models.CheckConstraint(
                condition=Q(weight__gt=0),
                name="assessment_weight_gt_0",
            ),
            models.UniqueConstraint(
                fields=[
                    "class_group",
                    "title",
                    "assessment_date",
                ],
                name="unique_assessment_class_title_date",
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.class_group}"


class Grade(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="grades",
    )

    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    feedback = models.TextField(
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
            "assessment",
            "student",
        )

        constraints = [
            models.CheckConstraint(
                condition=Q(score__gte=0),
                name="grade_score_gte_0",
            ),
            models.UniqueConstraint(
                fields=[
                    "assessment",
                    "student",
                ],
                name="unique_grade_per_assessment_student",
            ),
        ]

    def clean(self):
        super().clean()

        if not self.assessment_id or not self.student_id:
            return

        class_group = self.assessment.class_group

        is_enrolled = class_group.enrollments.filter(
            student=self.student,
            status=Enrollment.Status.ACTIVE,
        ).exists()

        if not is_enrolled:
            raise ValidationError(
                {
                    "student": (
                        "O aluno precisa estar matriculado "
                        "na turma desta avaliação."
                    )
                }
            )

        if self.score > self.assessment.max_score:
            raise ValidationError(
                {
                    "score": (
                        "A nota não pode ser maior que "
                        "a nota máxima da avaliação."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.student.registration_number} - "
            f"{self.assessment.title}: {self.score}"
        )