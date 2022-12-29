import os
import platform
from common import konstante
from collections import OrderedDict

platforma_var=platform.system()
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
    for parametar in formatiranje:
        red += f'{parametar:^{centriranje}} || '
    print(red)
    linija(len(red)-1)

    for row in podaci:
        red = '||'
        for item in row:
            item=str(item)
            red += f'{item:^{centriranje}} || '
        print(red)
        linija(len(red)-1,'-')


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