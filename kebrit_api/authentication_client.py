import uuid

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from kebrit_api.models import ClientApiToken


class ClientPrincipal:
    """
    Lightweight authenticated principal representing a customer (Company),
    used for client-token based authentication (not a student/admin user).
    """

    def __init__(self, company, token_uuid):
        self.company = company
        self.company_id = company.id
        self.token_uuid = token_uuid

    @property
    def is_authenticated(self):  # Django/DRF compatibility
        return True

    def __str__(self):
        return f"client:{self.company_id}"


class ClientTokenAuthentication(BaseAuthentication):
    """
    Auth via customer token.

    Supported headers:
    - X-Client-Token: <uuid>
    - Authorization: Token <uuid>
    """

    keyword = "Token"

    def authenticate(self, request):
        token = request.headers.get("X-Client-Token")
        if not token:
            auth = request.headers.get("Authorization", "")
            if auth:
                parts = auth.split()
                if len(parts) == 2 and parts[0] == self.keyword:
                    token = parts[1]

        if not token:
            return None

        try:
            token_uuid = uuid.UUID(str(token))
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid client token format")

        try:
            api_token = (
                ClientApiToken.objects.select_related("company")
                .get(uuid=token_uuid, is_active=True)
            )
        except ClientApiToken.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid or inactive client token")

        # Attach company for easy access in views
        request.auth_company = api_token.company
        request.auth_client_token = api_token

        principal = ClientPrincipal(api_token.company, token_uuid=str(api_token.uuid))
        return (principal, {"client_token": str(api_token.uuid), "company_id": api_token.company_id})

