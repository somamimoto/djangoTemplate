from django.urls import path
from . import views

app_name = 'csvapp'
urlpatterns = [
    path('import', views.csv_import, name='csv_import'),
    path('export', views.csv_export, name='csv_export'),
]