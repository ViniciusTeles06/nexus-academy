from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token


class GoogleTokenError(Exception):
    pass


def verify_google_token(token, client_id):
    try:
        payload = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            client_id,
        )
    except (ValueError, GoogleAuthError) as exc:
        raise GoogleTokenError(
            "Token do Google inválido."
        ) from exc

    email = payload.get("email")
    email_verified = payload.get(
        "email_verified",
        False,
    )

    if not email:
        raise GoogleTokenError(
            "O Google não retornou um e-mail."
        )

    if not email_verified:
        raise GoogleTokenError(
            "O e-mail do Google não está verificado."
        )

    return payload