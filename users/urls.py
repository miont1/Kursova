from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.profiles, name='profiles'),
    path('profile/<int:pk>/', views.userProfile, name='user-profile'),

    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, name='edit-account'),

    path('create-advantage/', views.createAdv, name='create-adv'),
    path('update-advantage/<str:pk>/', views.updateAdv, name='update-adv'),
    path('delete-advantage/<str:pk>/', views.deleteAdv, name='delete-adv'),

]
