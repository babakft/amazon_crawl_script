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

PRODUCT_ATTR = {"title": "a-size-medium a-color-base a-text-normal",
                "url": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal",
                "img": "s-image",
                "price": "true",
                "rate": "a-icon-alt",
                "section": "s-card-container s-overflow-hidden aok-relative"
                           " puis-include-content-margin puis s-latency-cf-section s-card-border"

                }

"""this argument are filled with user choices and than they are completely static in the whole project"""

STORAGE_TYPE = None
"""available storage type ["mongodb","file","csv]"""
DOWNLOAD_IMAGE = False

