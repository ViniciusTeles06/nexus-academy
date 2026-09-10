import uuid

from rest_framework.exceptions import NotFound, ValidationError

from .models import Membership


INSTITUTION_HEADER = "X-Institution-ID"


def get_current_membership(request):
    """
    Resolve a instituição ativa da requisição.

    O frontend envia:
    X-Institution-ID: <uuid-da-instituicao>
    """

    institution_id = request.headers.get(
        INSTITUTION_HEADER,
    )

    if not institution_id:
        raise ValidationError(
            {
                "institution": (
                    "O cabeçalho "
                    "X-Institution-ID é obrigatório."
                )
            }
        )

    try:
        institution_uuid = uuid.UUID(
            institution_id,
        )
    except (
        ValueError,
        TypeError,
        AttributeError,
    ):
        raise ValidationError(
            {
                "institution": (
                    "X-Institution-ID inválido."
                )
            }
        )

    try:
        membership = (
            Membership.objects
            .select_related(
                "institution",
                "user",
            )
            .get(
                user=request.user,
                institution_id=institution_uuid,
                status=Membership.Status.ACTIVE,
                institution__is_active=True,
            )
        )

    except Membership.DoesNotExist:
        raise NotFound(
            "Instituição não encontrada."
        )

    request.current_membership = (
        membership
    )

    request.current_institution = (
        membership.institution
    )

    return membership