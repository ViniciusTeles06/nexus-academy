from django.contrib import admin

from .models import AttendanceRecord, ClassSession


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = (
        "class_group",
        "date",
        "topic",
        "duration_minutes",
        "is_cancelled",
    )

    search_fields = (
        "topic",
        "class_group__code",
        "class_group__subject__name",
    )

    list_filter = (
        "date",
        "is_cancelled",
        "class_group__academic_period",
    )

    ordering = (
        "-date",
    )


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "session",
        "status",
        "updated_at",
    )

    search_fields = (
        "student__registration_number",
        "student__user__email",
        "student__user__first_name",
        "student__user__last_name",
        "session__topic",
        "session__class_group__code",
    )

    list_filter = (
        "status",
        "session__date",
        "session__class_group__academic_period",
    )