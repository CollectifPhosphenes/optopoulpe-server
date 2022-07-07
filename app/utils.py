import random

SAVES = (
    "dance",
    "doioweyou",
    "goodnight",
    "intro-ghost-town",
    "letithappen",
    "losingmymind",
    "reflections",
    "supersonic",
    "timhsupersonic",
    "vital1"
)


def reduce_int(int_value: int, ratio: int):
    return int(float(int_value) / ratio)


def get_random_save():
    return f"examples/{random.choice(SAVES)}.txt"
