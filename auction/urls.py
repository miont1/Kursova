from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.allAuctions, name='all_auctions'),
]
