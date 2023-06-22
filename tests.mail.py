from django.conf import settings
from django.core.mail import send_mail

print("Testing")

message = "Email test"
send_mail("subject", message, settings.EMAIL_HOST_USER, ["jonathanonderi2018@yahoo.com"],
          fail_silently=True, html_message=message)
