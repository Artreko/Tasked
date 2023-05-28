from datetime import datetime
from .crypt import password_encrypt
from json import dumps
from base64 import b64encode
from hashlib import md5
from .generate_key import generate_key
from dotenv import dotenv_values


config = {
    **dotenv_values('.env.secret'),
}

SECRET_KEY = config['SECRET_KEY']


def _sign_key(message: str) -> str:
    sign = md5(message.encode('utf-8')).hexdigest()
    message = (message + '.' + sign).encode()
    return b64encode(message).decode()


def _generate_crypted_key(message, key: str) -> str:
    message = password_encrypt(message, key)
    return _sign_key(message)


def make_encrypted_message(message):
    key = generate_key(SECRET_KEY)
    message = _generate_crypted_key(message, key)
    return message
