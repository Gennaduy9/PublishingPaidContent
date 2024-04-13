from django import forms
from django.core.exceptions import ValidationError

from publishings.models import Profile


class ClientForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'content', 'is_status')
        #widgets = {
        #    'is_status': forms.CheckboxInput()
        #}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Имя"})
        self.fields['last_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Фамилия"})
        self.fields['email'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Электронная почта"})
        self.fields['content'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Содержимое статьи"})

        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""
        self.fields['is_status'].label = 'Платный пост?'

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) > 30:
            raise ValidationError("Электронная почта может содержать не более 30 символов")
        if '@' not in email:
            raise ValidationError("Электронная почта невозможна без '@'.")
        return email