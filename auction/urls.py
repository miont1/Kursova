from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.allAuctions, name='all_auctions'),
    path('all/<str:auction_id>', views.singleAuction, name='single-auction'),

    path('create/', views.auctionCreate, name='create-auction'),
    path('update/<int:auction_id>/', views.auctionUpdate, name='update-auction'),
    path('delete/<int:auction_id>/', views.auctionDelete, name='delete-auction'),

    path('like-auction/<int:auction_id>/', views.like_auction, name='like-auction'),

]
