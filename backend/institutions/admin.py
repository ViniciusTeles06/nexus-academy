from django.contrib import admin

from .models import Institution, Membership


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "tax_id",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "legal_name",
        "slug",
        "tax_id",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "institution",
        "role",
        "status",
        "created_at",
    )

    list_filter = (
        "institution",
        "role",
        "status",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "institution__name",
    )

    autocomplete_fields = (
        "user",
        "institution",
    )