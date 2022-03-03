import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings


# send full logs to mail
def send_mail(body, recipients: list, subject):
    # setup email
    email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = email

    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email, password)

        for recipient in recipients:
            message["To"] = recipient
            server.sendmail(email, recipient, message.as_string())
