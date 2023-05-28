from base64 import b64encode
from hashlib import md5
from random import seed, choices, randint


def generate_key(serial_number: str, iterations: int = 100) -> str:
    seed(serial_number)
    for i in range(1, iterations+1):
        b64 = b64encode(serial_number.encode()).decode()[::-randint(i, iterations)]
        choice = ''.join(choices(list(b64), k=i+randint(i, iterations)))
        serial_number = md5(choice.encode()).hexdigest()
    return ''.join(choices(serial_number, k=len(serial_number)))
