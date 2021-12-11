import re


def email_exists(email):
    return True


def email_validator(email):
    if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) and email_exists(email):
        return True


def phone_number_validator(phone_number):
    return re.match(r"\+254\w{9}", phone_number)


def national_id_num_validator(national_id):
    return re.match(r"\[0-9]{8}", national_id)
