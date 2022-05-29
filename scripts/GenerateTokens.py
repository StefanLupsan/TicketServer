import string
import random


def generate_qr_link():
    return ''.join(random.choice(string.ascii_letters) for i in range(20))

