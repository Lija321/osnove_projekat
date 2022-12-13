import datetime
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
            "pasos": str(random.randint(100000000, 999999999)),
            "drzavljanstvo": rand_str(10),
            "telefon": str(random.randint(100000, 999999)),
            "pol": rand_str(10),
            "uloga": konstante.ULOGA_KORISNIK,
        }


def gen_rand_valid_users(num):
    for i in range(num):
        yield rand_valid_user()

def rand_date_str(**kwargs):
    start = datetime.date(2000, 1, 1) if "start" not in kwargs \
            else datetime.datetime.strptime(kwargs["start"], "%d.%m.%Y.").date()
    end = datetime.date(2023, 12, 31) if "end" not in kwargs \
        else datetime.datetime.strptime(kwargs["end"], "%d.%m.%Y.").date()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    date = start + datetime.timedelta(seconds=random_second)
    return date.strftime("%d.%m.%Y.")

def rand_time_str():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:0>2}:{minute:0>2}"

def rand_seat_positions():
    start = ord('A')
    # Dodaje se 1 da bi se izbegao slučaj gde je prazan red
    end = 1 + random.randint(ord('A'), ord('H'))
    return [chr(c) for c in range(start, end)]

def rand_seat():
    return f"{random.randint(ord('A'), )}"