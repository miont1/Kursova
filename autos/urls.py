from django.urls import path
from . import views

urlpatterns = [
    path('<int:auto_name>/', views.all_autos_info_number),
    path('<str:auto_name>/', views.all_autos_info, name='auto-name'),
]
