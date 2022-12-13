from common.konstante import PONEDELJAK,UTORAK,SREDA,CETVRTAK,PETAK,SUBOTA,NEDELJA
import json
from datetime import datetime, timedelta
import time

"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
*mislim da ne mora nista da vraca
todo
"""
def pregled_nerealizovanih_letova(svi_letovi: dict):
    pass

def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "", datum_polaska: str = "",datum_dolaska: str = "",
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "")->list:
    pass

def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str =""):
    pass

# 7 zad nema sad???
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: int):
    let={"broj_leta":broj_leta,"sifra_polazisnog_aerodroma":sifra_polazisnog_aerodroma, "sifra_odredisnog_aerodorma":sifra_odredisnog_aerodorma,
         "vreme_poletanja":vreme_poletanja,"vreme_sletanja":vreme_sletanja,
         "sletanje_sutra":sletanje_sutra,"prevoznik":prevoznik,"dani":dani,"model":model,"cena":cena}

    str_type=[broj_leta,sifra_odredisnog_aerodorma,sifra_polazisnog_aerodroma,prevoznik]
    dict_type=[svi_letovi,model]
    time_type=[vreme_sletanja,vreme_poletanja]
    bool_type=[sletanje_sutra]
    list_type=[dani]
    int_type=[cena]

    check_list=[(str_type,str),
                (dict_type,dict),
                (bool_type,bool),
                (list_type,list),
                (int_type,int)]

    for var_type_tuple in check_list:
        var_list=var_type_tuple[0]
        var_type=var_type_tuple[1]
        if not all(x for x in var_list):
            return f"{var_type} is empty"
        if not all(isinstance(x,var_type) for x in var_list):
            raise TypeError(var_type)

    time_error_raise=False
    for time_input in time_type:
        test1=False
        test2=False
        try:
            time.strptime(time_input,"%H:%M%p")
        except ValueError:
            test1=True
        try:
            time.strptime(time_input, "%H:%M")
        except ValueError:
            test2=True
        time_error_raise=time_error_raise or (test1 and test2)

    if time_error_raise: raise TypeError("time")





    svi_letovi[broj_leta]=let
    return svi_letovi

def izmena_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float)-> dict:
    if not (broj_leta in svi_letovi):
        raise  KeyError("let ne postoji")
        print(LookupError)


    let = {"broj_leta": broj_leta, "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,
           "sifra_odredisnog_aerodorma": sifra_odredisnog_aerodorma,
           "vreme_poletanja": vreme_poletanja, "vreme_sletanja": vreme_sletanja,
           "sletanje_sutra": sletanje_sutra, "prevoznik": prevoznik, "dani": dani, "model": model, "cena": cena}
    svi_letovi[broj_leta]=let
    return svi_letovi

def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    #['broj_leta', 'cena', 'dani', 'model', 'prevoznik',"sifra_odredisnog_aerodorma", 'sifra_polazisnog_aerodroma', 'sletanje_sutra', 'vreme_poletanja', 'vreme_sletanja']
    if not type(svi_letovi) is dict:
        # print("Greska")
        return "Greska: svi_letovi nije dict"

    with open(putanja, 'w') as f:
        for let in svi_letovi.items():

            nov_red=""
            let = let[1]

            let_keys=list(let.keys())
            let_keys.sort()
            for key in let_keys:
                nov_red+=str(let[key]).replace(',','~')+separator
            nov_red = nov_red[:-1] #oduzimanje bespotrebnog separatora
            nov_red+='\n'
            f.write(nov_red)


def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:

    with open(putanja, 'r') as f:
        letovi = f.readlines()

    letovi_return = {}

    for red in letovi:
        red = red.rstrip('\n')
        red = red.split(separator)

        broj_leta=red[0]
        cena=float(red[1])
        red[2]=red[2].replace('~',',')
        red[2]=red[2].replace("\'","")
        dani=red[2].strip('][').replace(" ","").split(',')
        red[3]=red[3].replace('~',',')
        model=json.loads(red[3].replace("\'","\""))
        prevoznik=red[4]
        sifra_odredisnog_aerodorma=red[5]
        sifra_polazisnog_aerodroma=red[6]
        sletanje_sutra=json.loads(red[7].lower())
        vreme_poletanja=red[8]
        vreme_sletanja=red[9]

        let = {"broj_leta": broj_leta, "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,"sifra_odredisnog_aerodorma":sifra_odredisnog_aerodorma,
               "vreme_poletanja": vreme_poletanja, "vreme_sletanja": vreme_sletanja,
               "sletanje_sutra": sletanje_sutra, "prevoznik": prevoznik, "dani": dani, "model": model, "cena": cena}
        letovi_return[broj_leta]=let
    return letovi_return


if __name__ == "__main__":
    svi_letovi={}
    kreiranje_letova(svi_letovi,"123","NCE","BEG","12:00","10:00AM",False,"WizzAir",[PONEDELJAK,SREDA,SUBOTA],{"marka":"Boing","sifra":"747"},25000)
