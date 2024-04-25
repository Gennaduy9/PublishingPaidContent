from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    # Форма регистрации пользователя
    class Meta:
        model = User  # Указываем модель пользователя для формы
        fields = ('phone',)  # Указываем поля, которые будут отображаться в форме

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Настройка атрибутов виджетов полей формы
        self.fields['phone'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите ваш номер телефона"})
        self.fields['password1'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Новый пароль"})
        self.fields['password2'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите пароль"})

        # Убираем метки и подсказки для полей
        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""


class UserLoginForm(AuthenticationForm):
    # Форма аутентификации пользователя
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Настройка атрибутов виджетов полей формы
        self.fields['username'].widget.attrs.update(
            {"class": "form-control", "id": "id_phone", "placeholder": "Напишите ваш номер телефона"})
        self.fields['password'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите ваш пароль"})

        # Убираем метки и подсказки для полей
        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""


class UserProfileForm(forms.ModelForm):
    # Форма профиля пользователя
    class Meta:
        model = User  # Указываем модель пользователя для формы
        fields = ('first_name', 'last_name', 'email', 'phone')  # Указываем поля, которые будут отображаться в форме

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Настройка атрибутов виджетов полей формы
        self.fields['first_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите ваше имя"})
        self.fields['last_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите вашу фамилию"})
        self.fields['email'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите свою почту"})
        self.fields['phone'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите свой телефон"})

        # Убираем метки и подсказки для полей
        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""


class PhoneAuthenticationForm(forms.Form):
    # Форма авторизации по телефону
    phone_number = forms.CharField(max_length=30, label='',
                                   widget=forms.TextInput(attrs={'class': 'w-100', 'placeholder': 'Телефон'}))
