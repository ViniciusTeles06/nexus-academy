from django.contrib import admin

from .models import Assessment, Grade


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "class_group",
        "assessment_type",
        "max_score",
        "weight",
        "assessment_date",
        "is_published",
    )

    search_fields = (
        "title",
        "class_group__code",
        "class_group__subject__name",
    )

    list_filter = (
        "assessment_type",
        "is_published",
        "assessment_date",
    )

    ordering = (
        "-assessment_date",
    )


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "assessment",
        "score",
        "updated_at",
    )

    search_fields = (
        "student__registration_number",
        "student__user__email",
        "student__user__first_name",
        "student__user__last_name",
        "assessment__title",
    )

    list_filter = (
        "assessment__assessment_type",
        "assessment__class_group__academic_period",
    )