from django.conf import settings
from django.db import transaction

from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.exceptions import (
    TokenError,
)
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)

from .models import User
from .serializers import (
    GoogleLoginSerializer,
    LoginSerializer,
    UserSerializer,
)
from .services.google_auth import (
    GoogleTokenError,
    verify_google_token,
)


def set_refresh_cookie(response, refresh_token):
    refresh_lifetime = settings.SIMPLE_JWT[
        "REFRESH_TOKEN_LIFETIME"
    ]

    response.set_cookie(
        key=settings.AUTH_COOKIE_NAME,
        value=str(refresh_token),
        max_age=int(
            refresh_lifetime.total_seconds()
        ),
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path=settings.AUTH_COOKIE_PATH,
    )


def delete_refresh_cookie(response):
    response.delete_cookie(
        key=settings.AUTH_COOKIE_NAME,
        path=settings.AUTH_COOKIE_PATH,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )


def create_auth_response(user):
    refresh = RefreshToken.for_user(user)

    response = Response(
        {
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        },
        status=status.HTTP_200_OK,
    )

    set_refresh_cookie(
        response,
        refresh,
    )

    return response


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.validated_data["user"]

        return create_auth_response(user)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = GoogleLoginSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        if not settings.GOOGLE_CLIENT_ID:
            return Response(
                {
                    "detail": (
                        "Login com Google ainda "
                        "não foi configurado."
                    )
                },
                status=(
                    status.HTTP_503_SERVICE_UNAVAILABLE
                ),
            )

        credential = serializer.validated_data[
            "credential"
        ]

        try:
            payload = verify_google_token(
                credential,
                settings.GOOGLE_CLIENT_ID,
            )
        except GoogleTokenError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = payload["email"].lower()

        first_name = payload.get(
            "given_name",
            "",
        )

        last_name = payload.get(
            "family_name",
            "",
        )

        avatar = payload.get(
            "picture",
            "",
        )

        user = User.objects.filter(
            email__iexact=email,
        ).first()

        if user is None:
            user = User.objects.create_user(
                email=email,
                password=None,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.STUDENT,
                avatar=avatar or None,
                is_email_verified=True,
            )

        else:
            fields_to_update = []

            if not user.is_active:
                return Response(
                    {
                        "detail": (
                            "Esta conta está desativada."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            if not user.is_email_verified:
                user.is_email_verified = True
                fields_to_update.append(
                    "is_email_verified"
                )

            if (
                avatar
                and not user.avatar
            ):
                user.avatar = avatar
                fields_to_update.append(
                    "avatar"
                )

            if (
                first_name
                and not user.first_name
            ):
                user.first_name = first_name
                fields_to_update.append(
                    "first_name"
                )

            if (
                last_name
                and not user.last_name
            ):
                user.last_name = last_name
                fields_to_update.append(
                    "last_name"
                )

            if fields_to_update:
                fields_to_update.append(
                    "updated_at"
                )

                user.save(
                    update_fields=fields_to_update,
                )

        return create_auth_response(user)


class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(
            settings.AUTH_COOKIE_NAME
        )

        if not refresh_token:
            return Response(
                {
                    "detail": (
                        "Refresh token não encontrado."
                    )
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = TokenRefreshSerializer(
            data={
                "refresh": refresh_token,
            }
        )

        try:
            serializer.is_valid(
                raise_exception=True,
            )
        except TokenError:
            return Response(
                {
                    "detail": (
                        "Refresh token inválido "
                        "ou expirado."
                    )
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {
                "access": (
                    serializer.validated_data[
                        "access"
                    ]
                ),
            },
            status=status.HTTP_200_OK,
        )

        rotated_refresh = (
            serializer.validated_data.get(
                "refresh"
            )
        )

        if rotated_refresh:
            set_refresh_cookie(
                response,
                rotated_refresh,
            )

        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(
            settings.AUTH_COOKIE_NAME
        )

        if refresh_token:
            try:
                token = RefreshToken(
                    refresh_token
                )

                token.blacklist()

            except TokenError:
                pass

        response = Response(
            status=status.HTTP_204_NO_CONTENT,
        )

        delete_refresh_cookie(response)

        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )