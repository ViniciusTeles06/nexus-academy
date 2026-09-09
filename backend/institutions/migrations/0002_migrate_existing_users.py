from django.db import migrations


DEFAULT_INSTITUTION_SLUG = "nexus-academy"


def migrate_existing_users(apps, schema_editor):
    User = apps.get_model(
        "accounts",
        "User",
    )

    Institution = apps.get_model(
        "institutions",
        "Institution",
    )

    Membership = apps.get_model(
        "institutions",
        "Membership",
    )

    institution, _ = (
        Institution.objects.get_or_create(
            slug=DEFAULT_INSTITUTION_SLUG,
            defaults={
                "name": "Nexus Academy",
                "legal_name": "",
                "tax_id": None,
                "is_active": True,
            },
        )
    )

    for user in User.objects.all().iterator():
        if user.is_superuser:
            role = "OWNER"

        elif user.role == "ADMIN":
            role = "ADMIN"

        elif user.role == "TEACHER":
            role = "TEACHER"

        else:
            role = "STUDENT"

        status = (
            "ACTIVE"
            if user.is_active
            else "INACTIVE"
        )

        Membership.objects.update_or_create(
            user_id=user.id,
            institution_id=institution.id,
            defaults={
                "role": role,
                "status": status,
            },
        )


def reverse_migration(apps, schema_editor):
    # Não apagamos vínculos automaticamente
    # em um rollback para evitar perda de dados.
    pass


class Migration(migrations.Migration):

    dependencies = [
        (
            "institutions",
            "0001_initial",
        ),
    ]

    operations = [
        migrations.RunPython(
            migrate_existing_users,
            reverse_migration,
        ),
    ]
