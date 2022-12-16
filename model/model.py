from datetime import datetime

def kreiraj_model_aviona(svi_modeli, id:int ,naziv:str ,broj_redova: int,pozicija_sedista: list) -> dict:
    model={"id":id,"naziv":naziv,"broj_redova":broj_redova,"pozicija_sedista":pozicija_sedista}
    svi_modeli[id]=model
    return svi_modeli

def vrati_sedista(model: dict) -> list:
    red=['X']*len(model["pozicija_sedista"])
    redovi=red*model[broj_redova]
    return redovi


# Dodato u if da se slučajno ne bi importovali u druge module
if __name__ == "__main__":
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
        "datum_kraja_operativnosti": datetime
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