import uuid

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class Institution(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=180,
    )

    slug = models.SlugField(
        max_length=180,
        unique=True,
        db_index=True,
    )

    legal_name = models.CharField(
        max_length=200,
        blank=True,
    )

    tax_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Membership(TimeStampedModel):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Proprietário"
        ADMIN = "ADMIN", "Administrador"
        COORDINATOR = "COORDINATOR", "Coordenador"
        TEACHER = "TEACHER", "Professor"
        STUDENT = "STUDENT", "Aluno"

    class Status(models.TextChoices):
        INVITED = "INVITED", "Convidado"
        ACTIVE = "ACTIVE", "Ativo"
        SUSPENDED = "SUSPENDED", "Suspenso"
        INACTIVE = "INACTIVE", "Inativo"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )

    class Meta:
        ordering = (
            "institution__name",
            "role",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "institution",
                ],
                name="unique_user_institution_membership",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "institution",
                    "role",
                ],
                name="membership_inst_role_idx",
            ),
            models.Index(
                fields=[
                    "user",
                    "status",
                ],
                name="membership_user_status_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.institution.name} - "
            f"{self.get_role_display()}"
        )