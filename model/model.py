from datetime import datetime
from ast import literal_eval



# Dodato u if da se slučajno ne bi importovali u druge module
if datetime.now==datetime(1999,1,1,1,1,1) and __name__ == "__main__": #Nikad nece doci
    let = {
        "broj_leta": str,
        "sifra_polazisnog_aerodroma": str,
        "sifra_odredisnog_aerodorma": str,
        "vreme_poletanja": str,
        "vreme_sletanja": str,
        "sletanje_sutra": bool,
        "prevoznik": str,
        "dani": str,
        "model": dict,
        "cena": float,
        "datum_pocetka_operativnosti": datetime,
        "datum_zavrsetka_operativnosti": datetime
    }
    konkretan_let ={
        "sifra": int,
        "broj_leta": str,
        "datum_i_vreme_polaska": datetime,
        "datum_i_vreme_dolaska": datetime,
        "zauzetost": iter, # bilo koja vrsta kolekcije koja je adekvatna
    }

    model_aviona = {
        "id": int,
        "naziv": str,
        "broj_redova": int,
        "pozicije_sedista": list #lista stringova
    }

    karta = {
        "broj_karte": int,
        "putnici": iter,
        "sifra_konkretnog_leta": int,
        "status": str,
        "obrisana": bool,
        "datum_prodaje": datetime,
        "prodavac": str,
        "kupac": str
    }