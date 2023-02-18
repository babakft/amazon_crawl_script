import string
import random

BASE_LINK_AMAZON = "https://www.amazon.com/s?k={}&page={}"


def header_generator():
    digit = random.choices(string.digits)
    punctuation = random.choices('!#$%&*:@^')
    uppercase = random.choices(string.ascii_uppercase, k=2)
    lowercase = random.choices(string.ascii_lowercase, k=2)
    password = digit + punctuation + uppercase + lowercase
    random.shuffle(password)
    return "".join(password)


HEADER = {
    'User-Agent': f"My User Agent {random.randint(2, 3)}.0",
    'From': header_generator() + '@gmail.com'
}

"""this argument are filled with user choices and than they are completely static in the whole project"""
"""available storage type ["mongodb","file","csv","redis"]"""
PROJECT_CONFIG = {"STORING": False,
                  "STORAGE_TYPE": None,
                  "DOWNLOAD_IMAGE": False}
