from django.urls import path
from . import views

app_name = 'zukan'
urlpatterns = [
    path('<slug:category_slug>/index/', views.index, name='index'),
    path('<slug:category_slug>/<slug:slug>/', views.detail, name='detail'),
]