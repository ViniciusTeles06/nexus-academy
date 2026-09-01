from rest_framework import serializers

from .models import Assessment, Grade


class AssessmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(
        source="class_group.subject.name",
        read_only=True,
    )

    class_code = serializers.CharField(
        source="class_group.code",
        read_only=True,
    )

    teacher_name = serializers.CharField(
        source="class_group.teacher.user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Assessment
        fields = (
            "id",
            "class_group",
            "class_code",
            "subject_name",
            "teacher_name",
            "title",
            "description",
            "assessment_type",
            "max_score",
            "weight",
            "assessment_date",
            "is_published",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "class_code",
            "subject_name",
            "teacher_name",
            "created_at",
            "updated_at",
        )


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.get_full_name",
        read_only=True,
    )

    registration_number = serializers.CharField(
        source="student.registration_number",
        read_only=True,
    )

    assessment_title = serializers.CharField(
        source="assessment.title",
        read_only=True,
    )

    subject_name = serializers.CharField(
        source="assessment.class_group.subject.name",
        read_only=True,
    )

    class Meta:
        model = Grade
        fields = (
            "id",
            "assessment",
            "assessment_title",
            "subject_name",
            "student",
            "student_name",
            "registration_number",
            "score",
            "feedback",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "assessment_title",
            "subject_name",
            "student_name",
            "registration_number",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        assessment = attrs.get(
            "assessment",
            getattr(self.instance, "assessment", None),
        )

        student = attrs.get(
            "student",
            getattr(self.instance, "student", None),
        )

        score = attrs.get(
            "score",
            getattr(self.instance, "score", None),
        )

        if assessment and score is not None:
            if score < 0:
                raise serializers.ValidationError(
                    {"score": "A nota não pode ser negativa."}
                )

            if score > assessment.max_score:
                raise serializers.ValidationError(
                    {
                        "score": (
                            "A nota não pode ser maior que "
                            "a nota máxima da avaliação."
                        )
                    }
                )

        if assessment and student:
            is_enrolled = (
                assessment.class_group.enrollments
                .filter(
                    student=student,
                    status="ACTIVE",
                )
                .exists()
            )

            if not is_enrolled:
                raise serializers.ValidationError(
                    {
                        "student": (
                            "O aluno não está matriculado "
                            "nesta turma."
                        )
                    }
                )

        return attrs