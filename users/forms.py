from django import forms

from .models import User
from .utils import validate_phone_number


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label='Подтверждение пароля'
    )

    class Meta:
        model = User
        fields = ['name', 'surname', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return password_confirm


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            normalized = validate_phone_number(phone)
            if User.objects.filter(phone=normalized).exclude(
                pk=self.instance.pk
            ).exists():
                raise forms.ValidationError(
                    'Этот номер телефона уже используется'
                )
            return normalized
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url:
            raise forms.ValidationError('Ссылка должна вести на GitHub')
        return url
