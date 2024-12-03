import random
import string


def generate_password(min_length=8, max_length=8):
    length = random.randint(min_length, max_length)
    password = generate_valid_password(length)
    return password


def generate_valid_password(length):
    password = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )

    if not any(char.isdigit() for char in password):
        return generate_valid_password(length)
    if not any(char.islower() for char in password):
        return generate_valid_password(length)
    if not any(char.isupper() for char in password):
        return generate_valid_password(length)

    return password
