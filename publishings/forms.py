from django import forms
from django.core.exceptions import ValidationError

from publishings.models import Profile


# Форма для создания и обновления профиля
class ClientForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('title', 'first_name', 'last_name', 'email', 'content', 'is_status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Обновление атрибутов виджетов для каждого поля
        self.fields['first_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Имя"})
        self.fields['last_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Фамилия"})
        self.fields['email'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Электронная почта"})
        self.fields['content'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Содержимое статьи", 'id': 'default-editor'})
        self.fields['title'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Заголовок статьи"})

        # Удаление меток и подсказок для каждого поля
        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""
        # Обновление метки для поля is_status
        self.fields['is_status'].label = 'Платный пост?'

    def clean_email(self):
        email = self.cleaned_data['email']
        # Проверка длины и формата электронной почты
        if len(email) > 30:
            raise ValidationError("Электронная почта может содержать не более 30 символов")
        if '@' not in email:
            raise ValidationError("Введите правильный адрес электронной почты.")
        return email

    def clean_content(self):
        content = self.cleaned_data['content']
        # Проверка длины содержимого
        if len(content) > 10000:  # Предполагается, что максимальная длина составляет 10000 символов
            raise forms.ValidationError("Содержимое статьи не может превышать 10000 символов.")
        return content

    def clean_title(self):
        title = self.cleaned_data['title']
        # Проверка длины содержимого
        if len(title) > 200:  # Предполагается, что максимальная длина составляет 1000 символов
            raise forms.ValidationError("Заголовок статьи превышает 200 символов.")
        return title