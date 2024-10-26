from django.forms import ModelForm
from .models import AutosModel


class AutoForm(ModelForm):
    class Meta:
        model = AutosModel
        fields = ['car_brand', 'car_model', 'description', 'demo_link', 'source_link', 'tags']
