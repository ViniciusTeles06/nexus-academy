from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Membership
from .permissions import HasActiveInstitution
from .serializers import MembershipSerializer


class MyMembershipListView(ListAPIView):
    serializer_class = MembershipSerializer

    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        return (
            Membership.objects
            .select_related(
                "institution",
            )
            .filter(
                user=self.request.user,
                status=Membership.Status.ACTIVE,
                institution__is_active=True,
            )
            .order_by(
                "institution__name",
            )
        )


class CurrentMembershipView(APIView):
    permission_classes = (
        IsAuthenticated,
        HasActiveInstitution,
    )

    def get(
        self,
        request,
    ):
        serializer = MembershipSerializer(
            request.current_membership,
        )

        return Response(
            serializer.data,
        )