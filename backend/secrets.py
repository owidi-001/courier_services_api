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

FIREBASE_CREDS = {
    "project_info": {
        "project_number": "551850869779",
        "project_id": "chess-1e75d",
        "storage_bucket": "chess-1e75d.appspot.com"
    },
    "client": [
        {
            "client_info": {
                "mobilesdk_app_id": "1:551850869779:android:5807dba255b78a68402be6",
                "android_client_info": {
                    "package_name": "com.example.courier"
                }
            },
            "oauth_client": [
                {
                    "client_id": "551850869779-qnft1jfusvl1ou7q0qm86us46gljdmta.apps.googleusercontent.com",
                    "client_type": 3
                }
            ],
            "api_key": [
                {
                    "current_key": "AIzaSyDyziXIAPxckpQxWDYPXW-zO4Y2-OL-weE"
                }
            ],
            "services": {
                "appinvite_service": {
                    "other_platform_oauth_client": [
                        {
                            "client_id": "551850869779-qnft1jfusvl1ou7q0qm86us46gljdmta.apps.googleusercontent.com",
                            "client_type": 3
                        }
                    ]
                }
            }
        }
    ],
    "configuration_version": "1"
}
