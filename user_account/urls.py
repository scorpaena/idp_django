from django.urls import path
from .views import signup_view, signup_login_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('signup_login/', signup_login_view, name='signup_login'),
]
