from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register_user/', views.register_user, name='register_user'),
    path('activate/<uid_b64>/<token>/', views.user_activate, name='user_activate'),
]