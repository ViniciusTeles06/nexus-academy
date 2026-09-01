from django.contrib import admin

from .models import (
    AcademicPeriod,
    ClassGroup,
    Course,
    Enrollment,
    StudentProfile,
    Subject,
    TeacherProfile,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "duration_semesters",
        "is_active",
        "created_at",
    )
    search_fields = ("name", "code")
    list_filter = ("is_active",)
    ordering = ("name",)


@admin.register(AcademicPeriod)
class AcademicPeriodAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("is_active",)
    ordering = ("-start_date",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "course",
        "semester",
        "workload_hours",
        "is_active",
    )
    search_fields = ("name", "code")
    list_filter = (
        "course",
        "semester",
        "is_active",
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "registration_number",
        "user",
        "course",
        "current_semester",
        "status",
    )
    search_fields = (
        "registration_number",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    list_filter = (
        "course",
        "status",
        "current_semester",
    )


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = (
        "employee_number",
        "user",
        "specialization",
        "is_active",
    )
    search_fields = (
        "employee_number",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    list_filter = ("is_active",)


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "subject",
        "academic_period",
        "teacher",
        "max_students",
        "is_active",
    )
    search_fields = (
        "code",
        "subject__name",
        "subject__code",
    )
    list_filter = (
        "academic_period",
        "is_active",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "class_group",
        "status",
        "enrolled_at",
    )
    list_filter = (
        "status",
        "class_group__academic_period",
    )
    search_fields = (
        "student__registration_number",
        "student__user__email",
        "class_group__code",
    )