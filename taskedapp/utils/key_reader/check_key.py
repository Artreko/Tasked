from base64 import b64decode
from hashlib import md5
from .crypt import password_decrypt
from .generate_key import generate_key
from dotenv import dotenv_values


config = {
    **dotenv_values('.env.secret'),
}

SECRET_KEY = config['SECRET_KEY']


def _check_sign(message: str, sign: str) -> bool:
    return md5(message.encode('utf-8')).hexdigest() == sign


def decode_key(message: str, key: str) -> str:
    message, sign = b64decode(message).decode().split('.')
    # print(message)
    message = password_decrypt(message, key)
    return message


def decrypt_message(message):
    key = generate_key(SECRET_KEY)
    return decode_key(message, key)
