from django.urls import path

from .views import (
    CurrentMembershipView,
    MyMembershipListView,
)


urlpatterns = [
    path(
        "mine/",
        MyMembershipListView.as_view(),
        name="my-institutions",
    ),

    path(
        "current/",
        CurrentMembershipView.as_view(),
        name="current-institution",
    ),
]