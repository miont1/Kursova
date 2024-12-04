from django import forms
from django.forms import ModelForm

from .models import Auction, AuctionCar, Bid


class CreateAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['end_time', 'start_price']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'start_price': 'Starting Price $',
            'end_time': 'Auction End Time'
        }

    def __init__(self, *args, **kwargs):
        super(CreateAuctionForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class AuctionCarForm(ModelForm):
    class Meta:
        model = AuctionCar
        fields = ['car_brand', 'car_model', 'description', 'featured_image']
        labels = {
            'car_brand': 'Car Brand',
            'car_model': 'Car Model',
            'featured_image': 'Image',
        }

    def __init__(self, *args, **kwargs):
        super(AuctionCarForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        labels = {
            'bid_amount': 'Your Bid'
        }

    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
