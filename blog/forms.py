from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from blog.models import Profile, Comment


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        }),
        required=False
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )

    class Meta:
        model = Comment
        exclude = ['created_on', 'post', 'user']

class AccountForm(forms.ModelForm):
    name = forms.CharField(help_text=' (Name)')
    surname = forms.CharField(help_text=' (Surname)')
    about_me = forms.CharField(help_text=' (About me)', required=False)
    avatar = forms.ImageField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ('name', 'surname', 'about_me', 'avatar')


class ExtendedRegisterForm(UserCreationForm):
    name = forms.CharField()
    surname = forms.CharField()
    about_me = forms.CharField(help_text='(Optional)', required=False)
    avatar = forms.ImageField(help_text='(Optional)', max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
