from django import forms

from users.form_validators import phone_number_validator, email_validator
from django.core.exceptions import ValidationError


class ClientProfileUpdateForm(forms.Form):
    avatar = forms.FileField(required=False)
    phone_number = forms.CharField(required=False, max_length=13)
    email = forms.EmailField(required=False)
    #gender = forms.CharField(max_length=1)

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
