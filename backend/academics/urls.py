from rest_framework.routers import DefaultRouter

from .views import (
    AcademicPeriodViewSet,
    ClassGroupViewSet,
    CourseViewSet,
    EnrollmentViewSet,
    SubjectViewSet,
)


router = DefaultRouter()

router.register(
    "courses",
    CourseViewSet,
    basename="course",
)

router.register(
    "periods",
    AcademicPeriodViewSet,
    basename="academic-period",
)

router.register(
    "subjects",
    SubjectViewSet,
    basename="subject",
)

router.register(
    "classes",
    ClassGroupViewSet,
    basename="class-group",
)

router.register(
    "enrollments",
    EnrollmentViewSet,
    basename="enrollment",
)


urlpatterns = router.urls