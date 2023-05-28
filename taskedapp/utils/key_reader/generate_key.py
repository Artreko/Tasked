from base64 import b64encode
from hashlib import md5
from random import seed, choices, randint


def generate_key(SECRET_KEY, iterations: int = 100) -> str:
    seed(SECRET_KEY)
    for i in range(1, iterations + 1):
        b64 = b64encode(SECRET_KEY.encode()).decode()[::-randint(i, iterations)]
        choice = ''.join(choices(list(b64), k=i+randint(i, iterations)))
        SECRET_KEY = md5(choice.encode()).hexdigest()
    return ''.join(choices(SECRET_KEY, k=len(SECRET_KEY)))
