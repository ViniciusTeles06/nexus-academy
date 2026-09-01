from rest_framework import serializers

from academics.models import Enrollment

from .models import AttendanceRecord, ClassSession


class ClassSessionSerializer(serializers.ModelSerializer):
    class_code = serializers.CharField(
        source="class_group.code",
        read_only=True,
    )

    subject_name = serializers.CharField(
        source="class_group.subject.name",
        read_only=True,
    )

    teacher_name = serializers.CharField(
        source="class_group.teacher.user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = ClassSession
        fields = (
            "id",
            "class_group",
            "class_code",
            "subject_name",
            "teacher_name",
            "date",
            "topic",
            "description",
            "duration_minutes",
            "is_cancelled",
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


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.get_full_name",
        read_only=True,
    )

    registration_number = serializers.CharField(
        source="student.registration_number",
        read_only=True,
    )

    class_code = serializers.CharField(
        source="session.class_group.code",
        read_only=True,
    )

    subject_name = serializers.CharField(
        source="session.class_group.subject.name",
        read_only=True,
    )

    session_date = serializers.DateField(
        source="session.date",
        read_only=True,
    )

    session_topic = serializers.CharField(
        source="session.topic",
        read_only=True,
    )

    class Meta:
        model = AttendanceRecord
        fields = (
            "id",
            "session",
            "session_date",
            "session_topic",
            "class_code",
            "subject_name",
            "student",
            "student_name",
            "registration_number",
            "status",
            "notes",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "session_date",
            "session_topic",
            "class_code",
            "subject_name",
            "student_name",
            "registration_number",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        session = attrs.get(
            "session",
            getattr(self.instance, "session", None),
        )

        student = attrs.get(
            "student",
            getattr(self.instance, "student", None),
        )

        if not session or not student:
            return attrs

        if session.is_cancelled:
            raise serializers.ValidationError(
                {
                    "session": (
                        "Não é possível registrar frequência "
                        "em uma aula cancelada."
                    )
                }
            )

        is_enrolled = Enrollment.objects.filter(
            student=student,
            class_group=session.class_group,
            status=Enrollment.Status.ACTIVE,
        ).exists()

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