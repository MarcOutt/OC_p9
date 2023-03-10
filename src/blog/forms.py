from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import PasswordInput, ClearableFileInput
from blog import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(max_length=63, widget=PasswordInput(attrs={'placeholder': 'Mot de passe'}), label="")


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)
        widgets = {'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'label': ''}),
                   'password1': forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'label': ''}),
                   'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmer mot de passe', 'label': ''})
                   }


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'blog/custom_clearable_file_input.html'


class TicketForm(forms.ModelForm):

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {'image': CustomClearableFileInput()}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {'rating': forms.RadioSelect(choices=[(i, i) for i in range(6)])}
