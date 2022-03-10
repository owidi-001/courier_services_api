class Config:
    def __init__(self):
        pass

    SECRET_KEY = "VOKEH"
    # email config

    # EMAIL_BACKEND = "django.core.mail.backends"
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = "mrmarangi4@gmail.com"
    EMAIL_HOST_PASSWORD = "rwgdxttcirhnwzrm"
    PORT = 465
    development = True
    ALLOWED_HOSTS = ["127.0.0.1", "courier-ke.herokuapp.com"]

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465



config = Config()
