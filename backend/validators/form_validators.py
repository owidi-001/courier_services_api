import re
from validate_email import validate_email

"""
 pyDNS library errors. install then replace return with `validate_email(email, verify=True)` To verify that email truely exists
"""


def email_exists(email):
    return validate_email(email)


def email_validator(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email) and email_exists(email)


def phone_number_validator(phone_number):
    pattern = r"\+254\w{9}"
    return re.match(pattern, phone_number)


def national_id_num_validator(national_id):
    pattern = r"(?<!\d)\d{8}(?!\d)"
    return re.match(pattern, national_id)

def license_validator(dl_number):
    return True
