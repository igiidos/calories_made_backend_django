from ninja import NinjaAPI
from ninja.security import django_auth, HttpBearer

from accounts.api import router as accounts_router
from calories.api import router as calories_router


api = NinjaAPI(title='칼로리메이드 API DOCS', version='1.0')


api.add_router("/accounts/", accounts_router, tags=['Auth'])
api.add_router("/calories/", calories_router, tags=['Calories'])


@api.get("/hello", tags=['Greeting'])
def hello(request):
    return "Hello world"


# class InvalidToken(Exception):
#     pass
#
#
# class GlobalAuth(HttpBearer):
#     def authenticate(self, request, token):
#         if token == "supersecret":
#             return token
#         raise InvalidToken
#
#
#
#
#
# @api.exception_handler(InvalidToken)
# def on_invalid_token(request, exc):
#     return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)
#
#
#
