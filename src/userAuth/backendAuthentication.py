from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class TokenBackendAuthentication(ModelBackend):

    def authenticate(self, request, username=None, token=None, **kwargs):

        try:
            user = get_user_model().objects.get(username=username)
            user_token = Token.objects.get(user=user)
            if user_token.key == token:
                user.is_active = True
                user.save()
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):

        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None


