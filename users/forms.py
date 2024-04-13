from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите ваш номер телефона"})
        self.fields['email'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите вашу электронную почту"})
        self.fields['password1'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Новый пароль"})
        self.fields['password2'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите пароль"})

        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {"class": "form-control", "id": "id_phone", "placeholder": "Напишите ваш номер телефона"})
        self.fields['password'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите ваш пароль"})

        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите ваше имя"})
        self.fields['last_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите вашу фамилию"})
        self.fields['phone'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите свой телефон"})

        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""


class PhoneAuthenticationForm(forms.Form):
    phone_number = forms.CharField(max_length=30, label='',
                                   widget=forms.TextInput(attrs={'class': 'w-100', 'placeholder': 'Телефон'}))
