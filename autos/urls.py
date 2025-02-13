from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_autos, name='all_autos'),
    path('api/', include('api.urls')),

    path('all_autos/<int:auto_number>/', views.all_autos_info_number, name='single-auto'),
    path('create-auto/', views.auto_create, name='create-auto'),
    path('update-auto/<str:pk>/', views.auto_update, name='update-auto'),
    path('delete-auto/<str:pk>/', views.auto_delete, name='delete-auto'),

]
