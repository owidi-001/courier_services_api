from django import forms

from users.form_validators import phone_number_validator, email_validator
from django.core.exceptions import ValidationError


class ClientProfileUpdateForm(forms.Form):
    username = forms.CharField(
        max_length=150, help_text="Username is required")
    phone_number = forms.CharField(required=False, max_length=13)
    email = forms.EmailField(required=False)
    is_driver = forms.BooleanField(required=False, help_text="I'm a driver")
    gender = forms.CharField(max_length=1, required=False)

    def clean_phone_number(self):
        phone_no = self.cleaned_data.get("phone_number")
        if phone_no and not phone_number_validator(phone_no):
            raise ValidationError(
                "please provide valid phone number eg +254712345678")
        return phone_no

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Please provide your email address")
        if not email_validator(email):
            raise ValidationError(
                "please provide a valid Email address")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise ValidationError("Username is required")
        return username

    def clean_is_driver(self):
        is_driver = self.cleaned_data.get("is_driver")
        if not is_driver:
            return False
        return True


class ClientAvatar(forms.Form):
    avatar = forms.ImageField(required=False)
