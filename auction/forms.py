from django import forms
from .models import Auction

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['start_price', 'start_time', 'end_time']
