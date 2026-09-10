from rest_framework import serializers

from .models import Institution, Membership


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution

        fields = (
            "id",
            "name",
            "slug",
            "is_active",
        )


class MembershipSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(
        read_only=True,
    )

    class Meta:
        model = Membership

        fields = (
            "id",
            "institution",
            "role",
            "status",
            "created_at",
        )