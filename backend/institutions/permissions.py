from rest_framework.permissions import BasePermission

from .context import get_current_membership


class HasActiveInstitution(BasePermission):
    message = (
        "Você não possui acesso "
        "a esta instituição."
    )

    def has_permission(
        self,
        request,
        view,
    ):
        get_current_membership(
            request,
        )

        return True