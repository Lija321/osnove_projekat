from datetime import datetime, date, timedelta

def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: datetime)->list:
    izvestaj_ret=[]
    #Prolazak kroz karte, ako je trazeni dan isti kao na karti -> dodaj tu kartu
    for karta in sve_karte.values():
        if 'datum_prodaje' in karta.keys():
            if isinstance(karta['datum_prodaje'],date) and karta['datum_prodaje']==dan:
                izvestaj_ret.append(karta)
            elif isinstance(karta['datum_prodaje'],datetime) and karta['datum_prodaje'].date()==dan:
                izvestaj_ret.append(karta)

    return izvestaj_ret
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date):
    izvestaj_ret = []
    # Prolazak kroz karte, ako je trazeni dan polaska isti kao na karti -> dodaj tu kartu
    for karta in sve_karte.values():
        sifra=karta['sifra_konkretnog_leta']
        let=svi_konkretni_letovi[sifra]
        if let['datum_i_vreme_polaska'].date() == dan:
            izvestaj_ret.append(karta)
    return izvestaj_ret

def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str):
    izvestaj_ret = []
    # Prolazak kroz karte, ako je trazeni dan isti kao na karti i prodavac isti -> dodaj tu kartu
    for karta in sve_karte.values():
        if karta['prodavac']==prodavac:
            if 'datum_prodaje' in karta.keys():
                if isinstance(karta['datum_prodaje'],date) and karta['datum_prodaje']==dan:
                    izvestaj_ret.append(karta)
                elif isinstance(karta['datum_prodaje'],datetime) and karta['datum_prodaje'].date()==dan:
                    izvestaj_ret.append(karta)
    return izvestaj_ret

def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:
    broj=0
    cena=0
    # Prolazak kroz karte, ako je trazeni dan isti kao na karti -> dodaj na akumulatore trazene parametre
    for karta in sve_karte.values():
        if (isinstance(karta['datum_prodaje'],datetime) and karta['datum_prodaje'].date()==dan) or \
                (isinstance(karta['datum_prodaje'],date) and karta['datum_prodaje']==dan):
            broj+=1
            sifra = karta['sifra_konkretnog_leta']
            konk_let = svi_konkretni_letovi[sifra]
            broj_leta=konk_let['broj_leta']
            let=svi_letovi[broj_leta]
            cena+=let['cena']
    return broj,cena




def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date): #ubc znaci ukupan broj i cena
    broj = 0
    cena = 0
    # Prolazak kroz karte, ako je trazeni dan polaska isti kao na karti -> dodaj na akumulatore trazene parametre
    for karta in sve_karte.values():
        sifra = karta['sifra_konkretnog_leta']
        let = svi_konkretni_letovi[sifra]
        dan_provere=let['datum_i_vreme_polaska'].date() #bitan je dan polaska ne vreme polasa; .date() uklanja vreme
        if isinstance(dan,datetime): dan_bez_sati=dan.date()
        else: dan_bez_sati=dan
        if dan_provere== dan_bez_sati:
            broj += 1
            sifra = karta['sifra_konkretnog_leta']
            konk_let = svi_konkretni_letovi[sifra]
            broj_leta = konk_let['broj_leta']
            let = svi_letovi[broj_leta]
            cena += let['cena']
    return broj, cena

def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date, prodavac: str): #ubc znaci ukupan broj i cena
    broj = 0
    cena = 0
    for karta in sve_karte.values():
        # Prolazak kroz karte, ako je trazeni dan isti kao na karti i prodavac -> dodaj na akumulatore trazene parametre
        if (isinstance(karta['datum_prodaje'],datetime) and karta['datum_prodaje'].date()==dan) or \
                (isinstance(karta['datum_prodaje'],date) and karta['datum_prodaje']==dan) \
                and karta['prodavac']==prodavac:
            broj += 1
            sifra = karta['sifra_konkretnog_leta']
            konk_let = svi_konkretni_letovi[sifra]
            broj_leta = konk_let['broj_leta']
            let = svi_letovi[broj_leta]
            cena += let['cena']
    return broj, cena

"""
Funkcija kao rezultat vraća rečnik koji za ključ ima dan prodaje, a za vrednost broj karata prodatih na taj dan.
Npr: {"2023-01-01": 20}
"""

def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict)->dict: #ubc znaci ukupan broj i cena

    datum_granica=datetime.now()
    datum_granica=datum_granica-timedelta(30) #Granica je poslednjih 30 dana
    ubc={}
    for karta in sve_karte.values():
        #"%d.%m.%Y."
        if not 'datum_prodaje' in karta.keys(): continue
        if isinstance(karta['datum_prodaje'] ,str):
            prosledjen_datum_datetime=datetime.strptime(karta['datum_prodaje'], "%d.%m.%Y.") #iz nekog razloga se ovako prosledjuje datum
        else: prosledjen_datum_datetime=karta['datum_prodaje']

        if prosledjen_datum_datetime<datum_granica: continue #ako je pre granice preskoci
        sifra = karta['sifra_konkretnog_leta']
        konk_let = svi_konkretni_letovi[sifra]
        broj_leta = konk_let['broj_leta']
        let = svi_letovi[broj_leta]
        cena = let['cena']
        prodavac=karta['prodavac']
        if isinstance(prodavac ,dict): prodavac=prodavac['korisnicko_ime']
        if prodavac in ubc.keys(): #Ako prodavac nije predjen prvi put dodaj na akumulatore
            ubc[prodavac][0]+=1
            ubc[prodavac][1]+=cena
        else:
            ubc[prodavac]= [1,cena,prodavac] #Ako je prvi put predjen dodaj ga u dict
    return ubc

    # noinspection PyUnreachableCode
    """
        ubc={}
        datum_granica = datetime.now()
        datum_granica = datum_granica - timedelta(30)  # Granica je poslednjih 30 dana
    
        for karta in sve_karte.values():
            # "%d.%m.%Y."
            prosledjen_datum=karta['datum_prodaje']
            prosledjen_datum_datetime = datetime.strptime(karta['datum_prodaje'],
                                                          "%d.%m.%Y.")  # iz nekog razloga se ovako prosledjuje datum
            if prosledjen_datum_datetime < datum_granica: continue  # ako je pre granice preskoci
            #sifra = karta['sifra_konkretnog_leta']
            #konk_let = svi_konkretni_letovi[sifra]
            #broj_leta = konk_let['broj_leta']
            #let = svi_letovi[broj_leta]
            #cena = let['cena']
            if not prosledjen_datum in ubc.keys():
                ubc[prosledjen_datum]=1
            else:
                ubc[prosledjen_datum] += 1
    
        return ubc
        """