from django.forms import ModelForm
from django import forms

from .models import AutosModel, AutoComment


class AutoForm(ModelForm):
    class Meta:
        model = AutosModel
        fields = ['car_brand', 'car_model', 'featured_image', 'price', 'description']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
        labels = {
            "price": "Price $",

        }

    def __init__(self, *args, **kwargs):
        super(AutoForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class CommentAutoForm(ModelForm):
    class Meta:
        model = AutoComment
        fields = ["value", "topic", "comment"]

        labels = {
            "value": "Give a vote",
            "topic": "Write a short topic",
            "comment": "Add a comment with your vote"
        }

    def __init__(self, *args, **kwargs):
        super(CommentAutoForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
