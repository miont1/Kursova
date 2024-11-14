from django.forms import ModelForm
from django import forms

from .models import AutosModel


class AutoForm(ModelForm):
    class Meta:
        model = AutosModel
        fields = ['car_brand', 'car_model', 'description', 'tags', 'featured_image']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(AutoForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
