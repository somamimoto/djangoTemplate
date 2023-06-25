from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register_user/', views.register_user, name='register_user'),
    path('activate/<uid_b64>/<token>/', views.user_activate, name='user_activate'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('validate_reset_password/<uid_b64>/<token>/', views.validate_reset_password, name='validate_reset_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('change_email/', views.change_email, name='change_email'),
    path('change_email_confirm/<uid_b64>/<token>/', views.change_email_confirm, name='change_email_confirm'),
    path('change_email_success/', views.change_email_success, name='change_email_success'),
]