from django import forms
from django.core.exceptions import ValidationError
from driver.models import Vehicle

from users.form_validators import phone_number_validator, email_validator, license_validator


# Driver
class DriverProfileUpdateForm(forms.Form):
    avatar = forms.FileField(required=False)
    phone_number = forms.CharField(required=False, max_length=13)
    email = forms.EmailField(required=False)
    gender = forms.CharField(max_length=1, required=False,)
    dl_number = forms.CharField(max_length=10, required=False)  # license No

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

    def clean_dl_number(self):
        dl_number = self.cleaned_data.get("dl_number")
        if not dl_number:
            raise ValidationError("Driver must have a driving license number")

        if not license_validator(dl_number):
            raise ValidationError(
                "Please provide a valid driving license number")

        return dl_number


class VehicleCreationForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["carrier_type", "carrier_capacity",
                  "vehicle_registration_number", "charge_rate"]
