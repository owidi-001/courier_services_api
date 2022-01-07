class Config:
    def __init__(self):
        pass

    SECRET_KEY = "VOKEH"
    # email config
    EMAIL_BACKEND = "django.core.mail.backends"
    EMAIL_USE_TLS = True
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = "mrmarangi4@gmail.com"
    EMAIL_HOST_PASSWORD = "pass"
    PORT = 465
    development = True
    ALLOWED_HOSTS = ["127.0.0.1"]


config = Config()
