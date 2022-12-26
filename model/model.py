from datetime import datetime
from ast import literal_eval

def kreiraj_model_aviona(svi_modeli, id:int ,naziv:str ,broj_redova: int,pozicija_sedista: list) -> dict:
    model={"id":id,"naziv":naziv,"broj_redova":broj_redova,"pozicija_sedista":pozicija_sedista}
    svi_modeli[id]=model
    sacuvaj_modele(svi_modeli,'./fajlovi/modeli.csv')
    return svi_modeli

def vrati_sedista(model: dict) -> list:
    red=['X']*len(model["pozicija_sedista"])
    redovi=[red]*model['broj_redova']
    return redovi

def sacuvaj_modele(svi_modeli,putanja):
    if not type(svi_modeli) is dict:
        raise Exception("Greska: svi_korisnici nije dict")
    with open(putanja, 'w') as f:
        for model in svi_modeli.values():
            red = str(model) + '\n'  # cuva red po red kao string
            f.write(red)
def ucitaj_modele(putanja: str, separator: str) -> dict:

    with open(putanja, 'r') as f:
        korisnici = f.readlines()

    model_ret = {}
    for red in korisnici:
        red = red.rstrip('\n')
        if red == '': continue
        model = literal_eval(str(red))  # safe eval svakog reda

        model_ret[model['id']]= model

    return model_ret

if __name__ =="__main__":
    kreiraj_model_aviona({},123,"Boing-747",20,['A','B','C','D'])


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
        "kupac": str,
        "sifra_sedista": str
    }