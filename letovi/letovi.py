import copy

from common.konstante import PONEDELJAK,UTORAK,SREDA,CETVRTAK,PETAK,SUBOTA,NEDELJA
import json
from ast import literal_eval
from datetime import datetime, timedelta, date
import time
from meni.meni import *

"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
def pregled_nerealizoivanih_letova(svi_letovi: dict):
    '''formatiranje = ['Broj leta', 'Polaziste', 'Odrediste', 'Vreme sletanja', 'Vreme poletanja', 'Sletanje sutra',
                    'Prevoznik', 'Dani leta', 'Cena']
    keys = ['broj_leta', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma',
            'vreme_sletanja','vreme_poletanja', 'sletanje_sutra', 'prevoznik',
            'dani', 'cena']
    podaci = []
    for let in svi_letovi.values():
        if let['datum_pocetka_operativnosti']>datetime.now():continue
        lista_leta = let_format_za_prikaz(let, keys)
        podaci.append(lista_leta)
    tabelarni_prikaz(podaci, formatiranje, 27)'''

    lista_leta=[]
    for let in svi_letovi.values():
        if let['datum_pocetka_operativnosti']<datetime.now():continue
        lista_leta.append(let)
    return lista_leta

"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi:dict, konkretan_let:dict): #SAMO BOG ZNA ZASTO
    broj_leta=konkretan_let['broj_leta']
    ret=copy.copy(svi_letovi[broj_leta]['model']['pozicije_sedista'])
    for i in range(0,len(ret)):
        ret[i]=False
    ret=[ret]*svi_letovi[broj_leta]['model']['broj_redova']
    konkretan_let['zauzetost']=ret
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
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "",
                    datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "") -> list:
    lista_kriterijuma=[(polaziste,"sifra_polazisnog_aerodroma",1), #1 za let, 0 za konkretan let
                       (odrediste,"sifra_odredisnog_aerodorma",1),
                       (datum_dolaska,'datum_i_vreme_dolaska',0), #konkreta
                       (datum_polaska,'datum_i_vreme_polaska',0), #konkretan
                       (vreme_poletanja,'vreme_poletanja',1),
                       (vreme_sletanja,'vreme_sletanja',1),
                       (prevoznik,'prevoznik',1)]
    letovi_ret=[]

    test_list=lista_kriterijuma[:] #Izbacivanje "" i None
    lista_kriterijuma=[]
    for provera in test_list:
        if not str(provera[0])=="" and not provera[0] is None:
            lista_kriterijuma.append(provera)

    for let in konkretni_letovi.values():
        ispunjava_filtere=True
        for item in lista_kriterijuma:
            val,key,id=item

            if id==0: #Nesto sto se nalazi u konkretnim letovima (datumi)
                if isinstance(val,str): #tipe je string
                    if isinstance(let[key],str) and val!=let[key]: #Ako je u recniku string -> poredi sa prosledjenim stringom
                        ispunjava_filtere=False

                    elif isinstance(let[key],str):
                        try:
                            datum = datetime.strptime(val, '%d.%m.%Y')
                        except ValueError:
                            raise Exception("Datumi pogresno unet")
                        ispunjava_filtere= datum.date()==let[key].date()

                elif let[key].date()!=val.date(): #ako je tipa datetime i nisu isti datumi
                    ispunjava_filtere = False

            elif id==1: #ako je iz letova / lower da bi bilo case insensitvie
                if not let['broj_leta'] in svi_letovi.keys():
                    ispunjava_filtere=False
                    continue
                if not svi_letovi[let['broj_leta']][key].lower()==val.lower():
                    ispunjava_filtere=False
                else:
                    pass

        if ispunjava_filtere:  #Ako nijedan filter nije pao -> dodaj
            letovi_ret.append(dict(let))
    return letovi_ret




def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str =""):
    filtrirani_letovi=[]
    odrediste_prazno= odrediste==''
    polaziste_prazno= polaziste==''
    for let in svi_letovi.values(): #Prvo uzmi one letovi sa datim polazistem
        if odrediste_prazno: odrediste=let["sifra_odredisnog_aerodorma"]
        if polaziste_prazno: polaziste=let["sifra_polazisnog_aerodroma"]

        if let["sifra_polazisnog_aerodroma"]==polaziste and let["sifra_odredisnog_aerodorma"]==odrediste:
            filtrirani_letovi.append(dict(let))

    #Sortiranje po ceni; iskreno ne znam kako radi
    sortirani_letovi=sorted(filtrirani_letovi, key=lambda i: i['cena'])

    sortirani_letovi=sortirani_letovi[::-1]
    #Ako ih je manje od 10 vrati sve
    if len(sortirani_letovi) <=10:
        return sortirani_letovi
    else: #Inace vrati prvih 10
        return sortirani_letovi[-10:]


def provera_validnosti_podatka_leta(broj_leta, sifra_odredisnog_aerodorma, sifra_polazisnog_aerodroma, prevoznik,
                                    svi_letovi, model,vreme_sletanja, vreme_poletanja,sletanje_sutra,dani,cena,
                                    datum_pocetka_operativnosti,datum_kraja_operativnosti):
    #Svi u listi istog tipa
    str_type = [broj_leta, sifra_odredisnog_aerodorma, sifra_polazisnog_aerodroma, prevoznik]
    dict_type = [svi_letovi, model]
    time_type = [vreme_sletanja, vreme_poletanja]
    bool_type = [sletanje_sutra]
    list_type = [dani]
    int_type = [cena]
    datetime_type = [datum_pocetka_operativnosti, datum_kraja_operativnosti]

    #Zajedno sa svojim tipom
    check_list = [(str_type, str),
                  (dict_type, dict),
                  (bool_type, bool),
                  (list_type, list),
                  (datetime_type, datetime)]

    #Idi krozlistu i proveri jel svaki dobrog tipa
    for var_type_tuple in check_list:
        var_list = var_type_tuple[0]
        var_type = var_type_tuple[1]
        #if not all(len(x)==0 for x in var_list):
        #    return f"{var_type} is empty"
        if not all(isinstance(x, var_type) for x in var_list):
            raise TypeError(f"{var_type} je nevalidan")

    time_error_raise = False #Provera vremean
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
        #Ako je pao oba testa (test1 and test2) ce biti true i zajedno sa or davace true do kraja
        time_error_raise = time_error_raise or (test1 and test2)
    if time_error_raise: raise TypeError("time")

    #Provera formata
    if not (broj_leta[:2].isalpha() and broj_leta[2:].isnumeric() and len(broj_leta) == 4):
        raise Exception("Nevalidan broj leta")
    if cena <= 0: raise Exception("Nevalidna cena") #Cena mora veca od nul3

    #Provera duzine
    if prevoznik=="": raise Exception("Nevalidan prevoznik")
    if len(dani)==0: raise Exception("Dani prazni")
    if len(sifra_polazisnog_aerodroma)!=3: raise Exception("Sifra polazisnog aerodroma neispravnog formata")
    if len(sifra_odredisnog_aerodorma) != 3: raise Exception("Sifra odredisnog aerodroma neispravnog formata")
    if not datum_pocetka_operativnosti < datum_kraja_operativnosti: raise Exception("Pocetak operativnosti pre kraja operativnosti")
    provera_validnosti_modela(model)
def provera_validnosti_modela(model):
    '''model_aviona_cmpr = {
        "id": int,
        "naziv": str,
        "broj_redova": int,
        "pozicije_sedista": list  # lista stringova
    }'''
    key_list=['id','naziv','broj_redova','pozicije_sedista']
    for key in key_list:
        if not key in model.keys(): raise Exception(f"Fali key {key} u modelu") #Provera jel su svi kljucevi tu

    #Provera jel sve kako treba
    if not isinstance(model['id'],int): raise TypeError('Id nije int')
    if model['naziv']=="": raise Exception('Naziv prazan string')
    if not model['broj_redova']>0: raise Exception('Greska u broju redova')
    # Ovaj drugi jel gleda dal su pozcije stringovi
    if model['pozicije_sedista']==[] and all(x.isalpha() for x in model['pozicije_sedista']): raise Exception('Greska u poziciji sedista')

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


    let = {"broj_leta": broj_leta, "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,
           "sifra_odredisnog_aerodorma": sifra_odredisnog_aerodorma,
           "vreme_poletanja": vreme_poletanja, "vreme_sletanja": vreme_sletanja,
           "sletanje_sutra": sletanje_sutra, "prevoznik": prevoznik, "dani": dani, "model": model, "cena": cena,
           "datum_pocetka_operativnosti": datum_pocetka_operativnosti,
           "datum_kraja_operativnosti": datum_kraja_operativnosti}

    provera_validnosti_podatka_leta(broj_leta, sifra_odredisnog_aerodorma, sifra_polazisnog_aerodroma, prevoznik,
                                    svi_letovi, model, vreme_sletanja, vreme_poletanja, sletanje_sutra, dani, cena,
                                    datum_pocetka_operativnosti, datum_kraja_operativnosti)
    svi_letovi[broj_leta] = let

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
    svi_letovi[broj_leta] = let

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
            let_keys.sort()#Da bi svaki put bilo isto
            for key in let_keys:
                #Ako je separator , moze nastati greska ako se cuva , pa se menja sa ~
                nov_red+=str(let[key]).replace(',','~')+separator
            nov_red = nov_red[:-1] #oduzimanje bespotrebnog separatora

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
        if red=='': continue
        red = red.split(separator)

        broj_leta=red[0]
        cena=float(red[1])
        red[2]=red[2].replace('~',',')#Vracanje , umesto ~
        red[2]=red[2].replace("\'","")#Da ne bi error izbacio
        dani=red[2].strip('][').replace(" ","").split(',')
        datum_kraja_operativnosti=datetime.strptime(red[3],"%Y-%m-%d %H:%M:%S")
        datum_pocetka_operativnosti=datetime.strptime(red[4],"%Y-%m-%d %H:%M:%S")
        red[5]=red[5].replace('~',',')
        model=literal_eval(red[5].replace("\'","\"")) #Ucita dict
        prevoznik=red[6]
        sifra_odredisnog_aerodorma=red[7]
        sifra_polazisnog_aerodroma=red[8]
        sletanje_sutra=json.loads(red[9].lower()) #Evaluira bool
        vreme_poletanja=red[10]
        vreme_sletanja=red[11]

        for i,dan in enumerate(dani):
            dani[i]=int(dan) #kad se dani ucitaju budu str

        let = {"broj_leta": broj_leta, "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,"sifra_odredisnog_aerodorma":sifra_odredisnog_aerodorma,
               "vreme_poletanja": vreme_poletanja, "vreme_sletanja": vreme_sletanja,
               "sletanje_sutra": sletanje_sutra, "prevoznik": prevoznik, "dani": dani, "model": model, "cena": cena,
               "datum_pocetka_operativnosti":datum_pocetka_operativnosti,"datum_kraja_operativnosti":datum_kraja_operativnosti}

        letovi_return[broj_leta]=let
    return letovi_return

"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""
def checkin(karta, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str) -> (dict, dict):
    if not konkretni_let['datum_i_vreme_polaska']-timedelta(hours=24) > datetime.now(): raise Exception("Check in prosao")


    red_index=red-1
    pozicija_sedista=copy.copy(svi_letovi[konkretni_let['broj_leta']]['model']['pozicije_sedista'])
    pozicija_index=pozicija_sedista.index(pozicija)

    zauzetost=copy.copy(konkretni_let['zauzetost'])

    if zauzetost[red_index][pozicija_index]==True: raise Exception("Mesto zauzeto")

    zauzetost[red_index][pozicija_index] = True
    karta['sediste']=str(pozicija)+str(red)

    return konkretni_let,karta


"""
Funkcija koja vraća listu konkretni letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""
def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    time_delta = timedelta(minutes=120)
    polaziste = svi_letovi[konkretni_let['broj_leta']]["sifra_odredisnog_aerodorma"]
    datum_polaska = konkretni_let['datum_i_vreme_dolaska']
    vreme_donja_granica = datum_polaska
    vreme_goranja_granica = datum_polaska + time_delta
    letovi_moguci = pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste, '', vreme_donja_granica)

    if not vreme_donja_granica.date() == vreme_goranja_granica.date():
        letovi_moguci += pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste, '', vreme_goranja_granica)

    temp_letovi = letovi_moguci[:]
    letovi_moguci = []
    for let in temp_letovi:
        datum_i_vreme_leta = let['datum_i_vreme_polaska']
        if vreme_donja_granica <= datum_i_vreme_leta <= vreme_goranja_granica:
            letovi_moguci.append(dict(let))

    return letovi_moguci


"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""
def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:
    moguci_letovi=pretraga_letova(svi_letovi,konkretni_letovi,polaziste,odrediste)
    opseg=timedelta(days=broj_fleksibilnih_dana)
    temp_letovi=moguci_letovi[:]
    moguci_letovi=[]
    donja_granica=datum_polaska-opseg
    goranja_granica=datum_polaska+opseg
    for let in temp_letovi:
        if donja_granica <= let['datum_i_vreme_polaska'] <= goranja_granica:
            moguci_letovi.append(let)

    return moguci_letovi




if __name__ == "__main__":
    pass