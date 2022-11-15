import random
import string
from common import konstante

def rand_str(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))

def rand_valid_user():
    return {
            "ime": rand_str(10),
            "prezime": rand_str(10),
            "korisnicko_ime": rand_str(10),
            "lozinka": rand_str(10),
            "email": f"{rand_str(10)}@email.com",
            "pasos": random.randint(100000000, 999999999),
            "drzavljanstvo": rand_str(10),
            "telefon": random.randint(100000, 999999),
            "pol": rand_str(10),
            "uloga": konstante.ULOGA_KORISNIK,
        }