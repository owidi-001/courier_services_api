from django import forms
from .models import User, Driver
from django.core.exceptions import ValidationError
from .form_validators import phone_number_validator, national_id_num_validator, email_validator, license_validator


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(help_text="Email is required")
    phone_number = forms.CharField(
        max_length=13, help_text="Phone number is required")
    national_id = forms.CharField(
        max_length=150, help_text="National id is required")

    class Meta:
        model = User
        fields = ["phone_number", "email", "national_id", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Please provide your email address")
        if not email_validator(email):
            raise ValidationError(
                "please provide a valid Email address")
        return email

    def clean_phone_number(self):
        phone_no = self.cleaned_data.get("phone_number")
        if not phone_no:
            raise ValidationError("please provide your phone number")
        if not phone_number_validator(phone_no):
            raise ValidationError(
                "please provide valid phone number eg +254712345678")
        return phone_no

    def clean_national_id(self):
        national_id = self.cleaned_data.get("national_id")
        if not national_id:
            raise ValidationError("please provide your national id number")
        if not national_id_num_validator(national_id):
            raise ValidationError(
                "please provide a valid national id number")
        return national_id

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)


class UserProfileUpdateForm(forms.Form):
    avatar = forms.FileField(required=False)
    phone_number = forms.CharField(required=False, max_length=13)
    email = forms.EmailField(required=False)

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


# Driver
class DriverProfileUpdateForm(forms.Form):
    avatar = forms.FileField(required=False)
    phone_number = forms.CharField(required=False, max_length=13)
    email = forms.EmailField(required=False)
    gender = forms.CharField(max_length=1)
    dl_number = forms.CharField(max_length=10)  # license No

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


class DriverCreationForm(forms.ModelForm):
    dl_number = forms.CharField(help_text="Your driver licence number")
    gender = forms.CharField(help_text="Gender")

    class Meta:
        model = Driver
        fields = ["dl_number", "gender"]