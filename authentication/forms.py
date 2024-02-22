import hashlib
from datetime import datetime
import pytz
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms

from authentication.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from tochkagpt import settings


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'chat-auth-input'
            field.widget.attrs['placeholder'] = ''
            field.widget.attrs['id'] = f'login-input-{field_name}'
            field.help_text = ''


class UserRegisterForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    email = forms.EmailField(required=True, label='Адрес электронной почты', )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'last_name', 'first_name', 'captcha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'captcha':
                field.widget.attrs['class'] = 'chat-auth-input'
                field.widget.attrs['placeholder'] = ''
                field.widget.attrs['id'] = f'register-input-{field_name}'
                field.help_text = ''

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.foreign_registration = False
        user.email_verified = False
        user.verification_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
        user.verification_key_expires = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()

        return user


class UserPasswordChangeForm(PasswordChangeForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2', 'captcha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''