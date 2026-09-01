from rest_framework.routers import DefaultRouter

from .views import AssessmentViewSet, GradeViewSet


router = DefaultRouter()

router.register(
    "assessments",
    AssessmentViewSet,
    basename="assessment",
)

router.register(
    "grades",
    GradeViewSet,
    basename="grade",
)


urlpatterns = router.urls