import os
import platform
from common import konstante
from collections import OrderedDict
from copy import copy

platforma_var=platform.system()

da_ne_dict={
        "da":True,
        'ne':False,
        "y":True,
        'n':False,
        'yes':True,
        'no':False,
        'd':True,
        'n':False,
        'true':True,
        'false':False
    }

def print_exception(msg):
    print(msg.__class__.__name__, msg)

def cls():
    if platforma_var=="Windows":os.system('cls')
    elif platforma_var=="Linux":os.system("clear")
    elif platforma_var.lower()=="darwin":os.system("clear")

def unesi(msg=''):
    ret=str(input(f"{msg} >>"))
    return ret

def linija(duzina=30,znak='='):
    print(znak*duzina)

def dict_to_list(dict,keys):
    lista_ret=[]
    for key in keys:
        lista_ret.append(dict[key])
    return lista_ret

def tabelarni_prikaz(podaci, formatiranje, centriranje=15):
    red = '||'
    if isinstance(centriranje,int):
        centriranje=[centriranje]*len(formatiranje)
    for parametar,cent in zip(formatiranje,centriranje):
        red += f'{parametar:^{cent}} || '
    print(red)
    linija(len(red)-1)

    for row in podaci:
        red = '||'
        for item,cent in zip(row,centriranje):
            item=str(item)
            red += f'{item:^{cent}} || '
        print(red)
        linija(len(red)-1,'-')

def prikaz_letova(letovi):
    formatiranje = ['Broj leta', 'Polaziste', 'Odrediste', 'Vreme sletanja', 'Vreme poletanja', 'Sletanje sutra',
                    'Prevoznik', 'Dani leta', 'Cena']
    keys = ['broj_leta', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma',
            'vreme_poletanja', 'vreme_sletanja', 'sletanje_sutra', 'prevoznik', 'dani', 'cena']
    podaci = []
    for let in letovi:
        lista_leta = let_format_za_prikaz(let, keys)
        podaci.append(copy(lista_leta))

    centriranje = [15] * 9
    centriranje[7] = 27
    tabelarni_prikaz(podaci, formatiranje, centriranje)

def prikaz_konkretnih_letova(letovi,svi_letovi):
    formatiranje = ['Sifra leta', 'Polaziste', 'Odrediste', 'Vreme sletanja', 'Vreme poletanja',
                    'Sletanje sutra',
                    'Prevoznik', 'Cena', 'Datum polaska', 'Datum dolaska']
    keys = ['sifra', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma',
            'vreme_poletanja', 'vreme_sletanja', 'sletanje_sutra', 'prevoznik',
            'cena', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska']


    podaci = []
    for let in letovi:
        lista_leta = konkretan_let_format_za_prikaz(let, keys, svi_letovi)
        podaci.append(lista_leta)
    tabelarni_prikaz(podaci, formatiranje, 15)

def dani_to_string(dani):
    dani_dict={
        konstante.PONEDELJAK: 'Pon',
        konstante.UTORAK: 'Uto',
        konstante.SREDA: 'Sre',
        konstante.CETVRTAK: 'Cet',
        konstante.PETAK: 'Pet',
        konstante.SUBOTA: 'Sub',
        konstante.NEDELJA: 'Ned'
    }
    ret=''
    for dan in dani:
        ret+=dani_dict[dan]+','
    ret=ret[:-1]
    return ret

def let_format_za_prikaz(let,keys):
    let_copy=dict(let)
    bool_to_da_ne_dict={True:"Da",False:'Ne'}
    let_copy['model'] = let_copy['model']['naziv']
    let_copy['datum_pocetka_operativnosti'] = let_copy['datum_pocetka_operativnosti'].date()
    let_copy['datum_kraja_operativnosti'] = let_copy['datum_kraja_operativnosti'].date()
    let_copy['dani'] = dani_to_string(let_copy['dani'])
    let_copy['sletanje_sutra']=bool_to_da_ne_dict[let_copy['sletanje_sutra']]
    lista_leta = dict_to_list(let_copy, keys)
    return lista_leta

def karta_format_za_prikaz(karta,keys,svi_letovi,svi_konkretni_letovi):
    karta_prikaz={}
    karta_prikaz['broj_karte']=copy(karta['broj_karte'])
    konkretan_let = copy(svi_konkretni_letovi[karta['sifra_konkretnog_leta']])
    let=copy(svi_letovi[konkretan_let['broj_leta']])
    karta_prikaz['sifra_polazisnog_aerodroma']=let['sifra_polazisnog_aerodroma']
    karta_prikaz['sifra_odredisnog_aerodorma']=let['sifra_odredisnog_aerodorma']
    karta_prikaz['vreme_sletanja']=let['vreme_sletanja']
    karta_prikaz['vreme_poletanja']=let['vreme_poletanja']
    karta_prikaz["datum_i_vreme_polaska"] = konkretan_let["datum_i_vreme_polaska"].date()
    karta_prikaz["datum_i_vreme_dolaska"] = konkretan_let["datum_i_vreme_dolaska"].date()
    lista_let = dict_to_list(karta_prikaz,keys)
    return lista_let


def konkretan_let_format_za_prikaz(konkreatan_let,keys,svi_letovi):
    konkreatan_let_copy=dict(konkreatan_let)
    let_copy=dict(svi_letovi[konkreatan_let_copy['broj_leta']])
    let_formatiran=konkreatan_let_copy | let_copy
    let_formatiran['model'] = let_copy['model']['naziv']
    bool_to_da_ne_dict={True:"Da",False:'Ne'}
    let_formatiran['model'] = let_copy['model']['naziv']
    let_formatiran['datum_pocetka_operativnosti'] = let_copy['datum_pocetka_operativnosti'].date()
    let_formatiran['datum_kraja_operativnosti'] = let_copy['datum_kraja_operativnosti'].date()
    let_formatiran['dani'] = dani_to_string(let_copy['dani'])
    let_formatiran['sletanje_sutra']=bool_to_da_ne_dict[let_copy['sletanje_sutra']]
    let_formatiran["datum_i_vreme_polaska"]=konkreatan_let_copy["datum_i_vreme_polaska"].date()
    let_formatiran['datum_i_vreme_dolaska']=konkreatan_let_copy['datum_i_vreme_dolaska'].date()
    lista_leta = dict_to_list(let_formatiran, keys)
    return lista_leta

def hasRepeatedChars(s):
    for i in xrange(len(s)):
        if i != s.rfind(s[i]):
            return True
    return False

def remove_duplicate(s):
    return "".join(OrderedDict.fromkeys(s))


if __name__=="__main__":
    pass