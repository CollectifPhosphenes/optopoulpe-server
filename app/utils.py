import random

SAVES = (
    "dance",
    "doioweyou",
    "goodnight",
    "intro-ghost-town",
    "letithappen",
    "losingmymind.txt",
    "reflections",
    "supersonic",
    "timhsupersonic",
    "vital"
)


def reduce_int(int_value: int, ratio: int):
    return int(float(int_value) / ratio)


def get_random_save():
    return f"{random.choice(SAVES)}.txt"
