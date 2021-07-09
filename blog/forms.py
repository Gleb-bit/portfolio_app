from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from blog.models import Profile, Comment, Post, Category


class CategoryDocumentForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class PostDocumentForm(forms.ModelForm):
    categories = forms.CharField(min_length=3, max_length=100, required=False,
                                 help_text='separated by space/через пробел')
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'categories')


class CommentForm(forms.ModelForm):
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
    image = forms.ImageField(required=False)

    class Meta:
        model = Comment
        exclude = ['created', 'post', 'user']


class AccountForm(forms.ModelForm):
    name = forms.CharField(help_text=' (Name)')
    surname = forms.CharField(help_text=' (Surname)')
    about_me = forms.CharField(help_text=' (About me)', required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('name', 'surname', 'about_me', 'avatar')


class ExtendedRegisterForm(UserCreationForm):
    name = forms.CharField(help_text="Имя")
    surname = forms.CharField(help_text='Фамилия')
    about_me = forms.CharField(help_text='Обо мне (Optional)', required=False)
    avatar = forms.ImageField(help_text='Аватар (Optional)', max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
