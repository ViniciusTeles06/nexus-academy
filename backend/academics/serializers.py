from rest_framework import serializers

from .models import (
    AcademicPeriod,
    ClassGroup,
    Course,
    Enrollment,
    StudentProfile,
    Subject,
    TeacherProfile,
)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "code",
            "duration_semesters",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class AcademicPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicPeriod
        fields = (
            "id",
            "name",
            "start_date",
            "end_date",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None),
        )

        end_date = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None),
        )

        if (
            start_date
            and end_date
            and end_date <= start_date
        ):
            raise serializers.ValidationError(
                {
                    "end_date": (
                        "A data final deve ser posterior "
                        "à data inicial."
                    )
                }
            )

        return attrs


class SubjectSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(
        source="course.name",
        read_only=True,
    )

    class Meta:
        model = Subject
        fields = (
            "id",
            "course",
            "course_name",
            "name",
            "code",
            "workload_hours",
            "semester",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "course_name",
            "created_at",
            "updated_at",
        )


class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )

    user_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    course_name = serializers.CharField(
        source="course.name",
        read_only=True,
    )

    class Meta:
        model = StudentProfile
        fields = (
            "id",
            "user",
            "user_name",
            "user_email",
            "course",
            "course_name",
            "registration_number",
            "admission_date",
            "current_semester",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user_name",
            "user_email",
            "course_name",
            "created_at",
            "updated_at",
        )


class TeacherProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )

    user_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = TeacherProfile
        fields = (
            "id",
            "user",
            "user_name",
            "user_email",
            "employee_number",
            "specialization",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user_name",
            "user_email",
            "created_at",
            "updated_at",
        )


class ClassGroupSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True,
    )

    teacher_name = serializers.CharField(
        source="teacher.user.get_full_name",
        read_only=True,
    )

    academic_period_name = serializers.CharField(
        source="academic_period.name",
        read_only=True,
    )

    enrolled_students = serializers.IntegerField(
        source="enrollments.count",
        read_only=True,
    )

    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "subject",
            "subject_name",
            "academic_period",
            "academic_period_name",
            "teacher",
            "teacher_name",
            "code",
            "max_students",
            "enrolled_students",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "subject_name",
            "academic_period_name",
            "teacher_name",
            "enrolled_students",
            "created_at",
            "updated_at",
        )


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.get_full_name",
        read_only=True,
    )

    registration_number = serializers.CharField(
        source="student.registration_number",
        read_only=True,
    )

    subject_name = serializers.CharField(
        source="class_group.subject.name",
        read_only=True,
    )

    class_code = serializers.CharField(
        source="class_group.code",
        read_only=True,
    )

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "student",
            "student_name",
            "registration_number",
            "class_group",
            "class_code",
            "subject_name",
            "status",
            "enrolled_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "student_name",
            "registration_number",
            "class_code",
            "subject_name",
            "enrolled_at",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        student = attrs.get(
            "student",
            getattr(self.instance, "student", None),
        )

        class_group = attrs.get(
            "class_group",
            getattr(self.instance, "class_group", None),
        )

        if (
            student
            and class_group
            and student.course_id
            != class_group.subject.course_id
        ):
            raise serializers.ValidationError(
                {
                    "class_group": (
                        "O aluno não pertence ao curso "
                        "desta disciplina."
                    )
                }
            )

        if (
            student
            and class_group
            and not self.instance
            and Enrollment.objects.filter(
                student=student,
                class_group=class_group,
            ).exists()
        ):
            raise serializers.ValidationError(
                "O aluno já está matriculado nesta turma."
            )

        return attrs