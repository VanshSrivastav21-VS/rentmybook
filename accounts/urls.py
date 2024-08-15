from django.urls import path
from .views import register, custom_login_view, custom_logout_view, profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('profile/', profile, name='profile'),
]
