from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_autos),
    path('all_autos/<int:auto_number>/', views.all_autos_info_number),
    path('all_autos/<str:auto_name>/', views.all_autos_info, name='single-auto'),
]
