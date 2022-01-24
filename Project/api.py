from ninja import NinjaAPI
from ninja.security import django_auth, HttpBearer

from accounts.api import router as accounts_router


class InvalidToken(Exception):
    pass


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token
        raise InvalidToken


api = NinjaAPI(auth=GlobalAuth(), csrf=True)


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


api.add_router("/accounts/", accounts_router)
