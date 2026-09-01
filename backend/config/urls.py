from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/v1/",
        include("accounts.urls"),
    ),

    path(
        "api/v1/academics/",
        include("academics.urls"),
    ),
]

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/v1/",
        include("accounts.urls"),
    ),

    path(
        "api/v1/academics/",
        include("academics.urls"),
    ),

    path(
        "api/v1/grading/",
        include("grading.urls"),
    ),

    path(
    "api/v1/attendance/",
    include("attendance.urls"),
    ),

]