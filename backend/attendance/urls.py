from rest_framework.routers import DefaultRouter

from .views import (
    AttendanceRecordViewSet,
    ClassSessionViewSet,
)


router = DefaultRouter()

router.register(
    "sessions",
    ClassSessionViewSet,
    basename="class-session",
)

router.register(
    "records",
    AttendanceRecordViewSet,
    basename="attendance-record",
)


urlpatterns = router.urls