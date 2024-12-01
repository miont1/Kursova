from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Advantage


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name": "Name"
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        self.fields['email'].required = True


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "username", "email", "profile_image", "bio", "shortbio",
                  "location", "social_telegram", "social_youtube"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class AdvantageForm(ModelForm):
    class Meta:
        model = Advantage
        fields = "__all__"
        exclude = ["owner"]

    def __init__(self, *args, **kwargs):
        super(AdvantageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
