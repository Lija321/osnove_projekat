from common.konstante import PONEDELJAK,UTORAK,SREDA,CETVRTAK,PETAK,SUBOTA,NEDELJA
import json
from datetime import datetime, timedelta
import time

import model

"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
def pregled_nerealizovanih_letova(svi_letovi: dict):
    pass

"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi:dict, konkretan_let:dict): #SAMO BOG ZNA ZASTO
    broj_leta=konkretan_let['broj_leta']
    ret=svi_letovi[broj_leta]['model']['pozicije_sedista']
    ret=[ret]*svi_letovi[broj_leta]['model']['broj_redova']
    return ret

"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""
def matrica_zauzetosti(konkretan_let): #SAMO BOG ZNA ZASTO
    if 'zauzetost' in konkretan_let:
        return konkretan_let['zauzetost']
    return []

"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "", datum_polaska: str = "",datum_dolaska: str = "",
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "")->list:
    lista_kriterijuma=[(polaziste,"sifra_polazisnog_aerodroma",1), #1 za let, 0 za konkretan let
                       (odrediste,"sifra_odredisnog_aerodorma",1),
                       (datum_dolaska,'datum_i_vreme_dolaska',0),
                       (datum_polaska,'datum_i_vreme_polaska',0),
                       (vreme_poletanja,'vreme_poletanja',1), #konkreta
                       (vreme_sletanja,'vreme_sletanja',1),   #konkretan
                       (prevoznik,'prevoznik',1)]
    letovi_ret=[]

    test_list=lista_kriterijuma[:]
    lista_kriterijuma=[]
    for provera in test_list:
        if str(provera[0])!="":
            lista_kriterijuma.append(provera)




    for let in konkretni_letovi.values():
        ispunjava_filtere=True
        for item in lista_kriterijuma:
            val,key,id=item
            if id==0 and let[key] != val:
                ispunjava_filtere=False
            elif id==1:
                if not svi_letovi[let['broj_leta']][key]==val:
                    ispunjava_filtere==False


        if ispunjava_filtere:
            letovi_ret.append(let)
    return letovi_ret




#IZBIRSANO SA GITLABA
def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str =""):
    filtrirani_letovi=[]
    for let in svi_letovi.values():
        if let["sifra_polazisnog_aerodroma"]==polaziste and let["sifra_odredisnog_aerodorma"]==odrediste:
            filtrirani_letovi.append(let)
    sortirani_letovi=sorted(filtrirani_letovi, key=lambda i: i['cena'])
    if len(sortirani_letovi) <=10:
        return sortirani_letovi
    else:
        return sortirani_letovi[:11]


def provera_validnosti_podatka_leta(broj_leta, sifra_odredisnog_aerodorma, sifra_polazisnog_aerodroma, prevoznik,
                                    svi_letovi, model,vreme_sletanja, vreme_poletanja,sletanje_sutra,dani,cena,
                                    datum_pocetka_operativnosti,datum_kraja_operativnosti):
    str_type = [broj_leta, sifra_odredisnog_aerodorma, sifra_polazisnog_aerodroma, prevoznik]
    dict_type = [svi_letovi, model]
    time_type = [vreme_sletanja, vreme_poletanja]
    bool_type = [sletanje_sutra]
    list_type = [dani]
    int_type = [cena]
    datetime_type = [datum_pocetka_operativnosti, datum_kraja_operativnosti]

    check_list = [(str_type, str),
                  (dict_type, dict),
                  (bool_type, bool),
                  (list_type, list),
                  (datetime_type, datetime)]
    for var_type_tuple in check_list:
        var_list = var_type_tuple[0]
        var_type = var_type_tuple[1]
        # if not all(x for x in var_list):
        #    return f"{var_type} is empty"
        if not all(isinstance(x, var_type) for x in var_list):
            raise TypeError(f"{var_type} je nevalidan")
    time_error_raise = False
    for time_input in time_type:
        test1 = False
        test2 = False
        try:
            time.strptime(time_input, "%H:%M%p")
        except ValueError:
            test1 = True
        try:
            time.strptime(time_input, "%H:%M")
        except ValueError:
            test2 = True
        time_error_raise = time_error_raise or (test1 and test2)
    if time_error_raise: raise TypeError("time")

    if not (broj_leta[:2].isalpha() and broj_leta[2:].isnumeric() and len(broj_leta) == 4):
        raise Exception("Nevalidan broj leta")
    if cena <= 0:
        raise Exception("Nevalidna cena")

    if len(sifra_polazisnog_aerodroma)!=3: raise Exception("Sifra polazisnog aerodroma neispravnog formata")
    if len(sifra_odredisnog_aerodorma) != 3: raise Exception("Sifra odredisnog aerodroma neispravnog formata")



"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: int,datum_pocetka_operativnosti: datetime, datum_kraja_operativnosti: datetime):
    let={"broj_leta":broj_leta,"sifra_polazisnog_aerodroma":sifra_polazisnog_aerodroma, "sifra_odredisnog_aerodorma":sifra_odredisnog_aerodorma,
         "vreme_poletanja":vreme_poletanja,"vreme_sletanja":vreme_sletanja,
         "sletanje_sutra":sletanje_sutra,"prevoznik":prevoznik,"dani":dani,"model":model,"cena":cena,
         "datum_pocetka_operativnosti":datum_pocetka_operativnosti,"datum_kraja_operativnosti":datum_kraja_operativnosti}

    str_type=[broj_leta,sifra_odredisnog_aerodorma,sifra_polazisnog_aerodroma,prevoznik]
    dict_type=[svi_letovi,model]
    time_type=[vreme_sletanja,vreme_poletanja]
    bool_type=[sletanje_sutra]
    list_type=[dani]
    int_type=[cena]
    datetime_type=[datum_pocetka_operativnosti,datum_kraja_operativnosti]

    check_list=[(str_type,str),
                (dict_type,dict),
                (bool_type,bool),
                (list_type,list),
                (datetime_type,datetime)]
    for var_type_tuple in check_list:
        var_list=var_type_tuple[0]
        var_type=var_type_tuple[1]
        #if not all(x for x in var_list):
        #    return f"{var_type} is empty"
        if not all(isinstance(x,var_type) for x in var_list):
            raise TypeError(f"{var_type} je nevalidan")
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

    if not(broj_leta[:2].isalpha() and broj_leta[2:].isnumeric() and len(broj_leta)==4):
        raise Exception("Nevalidan broj leta")
    if cena <=0:
        raise Exception("Nevalidna cena")


    svi_letovi[broj_leta]=let
    return svi_letovi

"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def izmena_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float,datum_pocetka_operativnosti: datetime,
    datum_kraja_operativnosti: datetime )-> dict:
    if not (broj_leta in svi_letovi):
        raise  KeyError("let ne postoji")


    let = {"broj_leta": broj_leta, "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,
           "sifra_odredisnog_aerodorma": sifra_odredisnog_aerodorma,
           "vreme_poletanja": vreme_poletanja, "vreme_sletanja": vreme_sletanja,
           "sletanje_sutra": sletanje_sutra, "prevoznik": prevoznik, "dani": dani, "model": model, "cena": cena,
           "datum_pocetka_operativnosti":datum_pocetka_operativnosti,"datum_kraja_operativnosti":datum_kraja_operativnosti}

    provera_validnosti_podatka_leta(broj_leta, sifra_odredisnog_aerodorma, sifra_polazisnog_aerodroma, prevoznik,
                                    svi_letovi, model,vreme_sletanja, vreme_poletanja,sletanje_sutra,dani,cena,
                                    datum_pocetka_operativnosti,datum_kraja_operativnosti)

    for key in let.keys():
        svi_letovi[broj_leta][key]=let[key]
    return svi_letovi

"""
Funkcija koja cuva sve letove na zadatoj putanji
"""
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
            nov_red = nov_red[:-1] #oduzimanje bespotrebnog separatora"""

            nov_red+='\n'
            f.write(nov_red)

"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""
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
        datum_kraja_operativnosti=datetime.strptime(red[3],"%Y-%m-%d %H:%M:%S")
        datum_pocetka_operativnosti=datetime.strptime(red[4],"%Y-%m-%d %H:%M:%S")
        red[5]=red[5].replace('~',',')
        model=json.loads(red[5].replace("\'","\""))
        prevoznik=red[6]
        sifra_odredisnog_aerodorma=red[7]
        sifra_polazisnog_aerodroma=red[8]
        sletanje_sutra=json.loads(red[9].lower())
        vreme_poletanja=red[10]
        vreme_sletanja=red[11]

        for i,dan in enumerate(dani):
            dani[i]=int(dan)


        let = {"broj_leta": broj_leta, "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,"sifra_odredisnog_aerodorma":sifra_odredisnog_aerodorma,
               "vreme_poletanja": vreme_poletanja, "vreme_sletanja": vreme_sletanja,
               "sletanje_sutra": sletanje_sutra, "prevoznik": prevoznik, "dani": dani, "model": model, "cena": cena,
               "datum_pocetka_operativnosti":datum_pocetka_operativnosti,"datum_kraja_operativnosti":datum_kraja_operativnosti}

        letovi_return[broj_leta]=let
    return letovi_return


if __name__ == "__main__":
    pass