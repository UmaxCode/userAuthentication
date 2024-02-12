from django.urls import path
from .views import user_signup, user_login_up, user_login_ut


urlpatterns = [
    path('auth_signup', user_signup, name='signup'),
    path('auth_login', user_login_up, name='login'),
    path('auth_login_token', user_login_ut, name='token_login')
]
