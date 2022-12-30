import copy
import os
import random
import unittest

from random import randint

from common import konstante
from letovi import letovi

from test.test_utils import rand_str, rand_valid_user, rand_time_str, rand_seat_positions, rand_datetime
from datetime import datetime, timedelta


# 1. Test case po stavci iz projekta
# 2. Konvencija imenovanja (test_kreiraj_* za kreiranje) i svi scenariji u jednom testu
# 3. Konvencija imenovanja (test_kreiraj_* za kreiranje) ali su scenariji razdvojeni. Npr. prazno ime i prazan email posebni testovi
class LetoviTest(unittest.TestCase):
    def setUp(self):
        self.modeli_aviona = {
            123: {
                "id": 123,
                "naziv": rand_str(10),
                "broj_redova": random.randint(20, 50),
                "pozicije_sedista": rand_seat_positions()
            },
            124: {
                "id": 124,
                "naziv": rand_str(10),
                "broj_redova": random.randint(20, 50),
                "pozicije_sedista": rand_seat_positions()
            }
        }

        broj_leta = rand_str(2) + str(randint(10,99))

        self.konkretan_let = {
            "sifra": 1234,
            "broj_leta": broj_leta,
            "datum_i_vreme_polaska": rand_datetime(),
            "datum_i_vreme_dolaska": rand_datetime()
        }
        dani = list({random.randint(0, 6): True for n in range(random.randint(1, 7))}.keys())
        dani.sort()
        pocetak_operativnosti = rand_datetime()
        kraj_operativnosti = pocetak_operativnosti + timedelta(days=10)
        self.pun_let = {
            "broj_leta": broj_leta,
            "sifra_polazisnog_aerodroma": rand_str(3),
            "sifra_odredisnog_aerodorma": rand_str(3),
            "vreme_poletanja": rand_time_str(),
            "vreme_sletanja": rand_time_str(),
            "datum_pocetka_operativnosti": pocetak_operativnosti,
            "datum_kraja_operativnosti": kraj_operativnosti,
            "sletanje_sutra": False,
            "prevoznik": rand_str(10),
            "dani": dani,
            "model": self.modeli_aviona[123],
            "cena": 100 + random.random() * 200
        }
        self.pun_korisnik = rand_valid_user()
        self.svi_letovi = {
            broj_leta: self.pun_let
        }

        self.putanja = "test_letovi.csv"

        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_kreiraj_let_validan(self):
        svi_letovi = letovi.kreiranje_letova(
            {},
            self.pun_let["broj_leta"],
            self.pun_let["sifra_polazisnog_aerodroma"],
            self.pun_let["sifra_odredisnog_aerodorma"],
            self.pun_let["vreme_poletanja"],
            self.pun_let["vreme_sletanja"],
            self.pun_let["sletanje_sutra"],
            self.pun_let["prevoznik"],
            self.pun_let["dani"],
            self.pun_let["model"],
            self.pun_let["cena"],
            self.pun_let["datum_pocetka_operativnosti"],
            self.pun_let["datum_kraja_operativnosti"]
        )
        self.assertIsNotNone(svi_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], svi_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            svi_letovi[self.pun_let["broj_leta"]],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_kreiraj_let_prazan(self):
        for key in self.pun_let:
            let = copy.deepcopy(self.pun_let)
            let[key] = ""
            let["model"] = 0
            let["cena"] = 0
            with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: broj leta"):
                rezultat = letovi.kreiranje_letova(
                    {},
                    let["broj_leta"],
                    let["sifra_polazisnog_aerodroma"],
                    let["sifra_odredisnog_aerodorma"],
                    let["vreme_poletanja"],
                    let["vreme_sletanja"],
                    let["sletanje_sutra"],
                    let["prevoznik"],
                    let["dani"],
                    let["model"],
                    let["cena"],
                    let["datum_pocetka_operativnosti"],
                    let["datum_kraja_operativnosti"]
                )

    def test_kreiraj_let_nevalidan_broj_leta(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: broj leta"):
            rezultat = letovi.kreiranje_letova(
                {},
                rand_str(7),
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_kreiraj_let_nevalidno_vreme_polaska(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: vreme polaska"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                rand_str(8),
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_kreiraj_let_nevalidno_vreme_dolaska(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: vreme dolaska"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                rand_str(2),
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )


    def test_kreiraj_let_nevalidni_dani(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: losi dani"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                [],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_kreiraj_let_nevalidna_cena(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: cena"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                randint(-100,-1),
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_kreiraj_let_nevalidan_model(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: model"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                {},
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
                )


    def test_kreiraj_let_pocetak_pre_kraja(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: pocetak pre kraja"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                # kraj i pocetak su promenili redosled
                self.pun_let["datum_kraja_operativnosti"],
                self.pun_let["datum_pocetka_operativnosti"]
            )

    #--------------------------------------------------------------
    def test_pretraga_letova_uspesno_po_polazistu(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]:self.konkretan_let},
            self.pun_let["sifra_polazisnog_aerodroma"]
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertDictEqual(
            self.konkretan_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_pretraga_letova_uspesna_po_odredistu(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            self.pun_let["sifra_odredisnog_aerodorma"]
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertDictEqual(
            self.konkretan_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_pretraga_letova_uspesna_po_datumu_polaska(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            None,
            None,
            self.konkretan_let["datum_i_vreme_polaska"],
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertDictEqual(
            self.konkretan_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_pretraga_letova_uspesna_po_datumu_dolaska(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            None,
            self.konkretan_let["datum_i_vreme_dolaska"]
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertDictEqual(
            self.konkretan_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_pretraga_letova_uspesna_po_vremenu_poletanja(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            None,
            None,
            self.pun_let["vreme_poletanja"],
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")

        self.assertDictEqual(
            self.konkretan_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_pretraga_letova_uspesna_po_vremenu_sletanja(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            None,
            None,
            "",
            self.pun_let["vreme_sletanja"],
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertDictEqual(
            self.konkretan_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_pretraga_letova_uspesna_po_prevozniku(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            None,
            None,
            "",
            "",
            self.pun_let["prevoznik"],
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertDictEqual(
            self.konkretan_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_pretraga_letova_visekriterijumska_uspesna(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            self.pun_let["sifra_polazisnog_aerodroma"],
            self.pun_let["sifra_odredisnog_aerodorma"],
            None,
            None,
            self.pun_let["vreme_poletanja"],
            self.pun_let["vreme_sletanja"],
            self.pun_let["prevoznik"],

           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertDictEqual(
            self.konkretan_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )


    def test_pretraga_letova_neuspesna(self):
        with self.assertRaises(Exception, msg=f"Neuspesno trazenje leta"):
            trazeni_letovi = letovi.pretraga_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                {self.konkretan_let["sifra"]: self.konkretan_let},
                rand_str(3),
                rand_str(3),
                None,
                None,
                rand_str(5),
                self.pun_let["sifra_vreme_sletanja"],
                self.pun_let["prevoznik"])

    #--------------------------------------------------------------
    def test_trazenje_10_najjeftinijih_letova_uspesno(self):

        svi_letovi = self.get_letovi()
        lista = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, "", "")
        self.assertIsNotNone(lista, msg="Nije vraćena kolekcija letova")
        self.assertTrue(len(lista)<=10, msg="Ima previse elemenata liste")
        self.assertDictEqual(
            svi_letovi["aa44"],
            lista[0],
            msg="Vrednosti od leta nisu dobre"
        )
    def test_trazenje_10_najjeftinijih_letova_uspesno_sa_polazistem(self):

        svi_letovi = self.get_letovi()
        lista = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, svi_letovi["aa44"]["sifra_polazisnog_aerodroma"], "")
        self.assertIsNotNone(lista, msg="Nije vraćena kolekcija letova")
        self.assertTrue(len(lista)<=10, msg="Ima previse elemenata liste")
        self.assertDictEqual(
            svi_letovi["aa44"],
            lista[0],
            msg="Vrednosti od leta nisu dobre"
        )
    def test_trazenje_10_najjeftinijih_letova_uspesno_sa_odredistem(self):
        svi_letovi = self.get_letovi()
        lista = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, "", svi_letovi["aa44"]["sifra_odredisnog_aerodorma"])
        self.assertIsNotNone(lista, msg="Nije vraćena kolekcija letova")
        self.assertTrue(len(lista)<=10, msg="Ima previse elemenata liste")
        self.assertDictEqual(
            svi_letovi["aa44"],
            lista[0],
            msg="Vrednosti od leta nisu dobre"
        )
    def test_trazenje_10_najjeftinijih_letova_uspesno_sa_odredistem_i_polazistem(self):
        svi_letovi = self.get_letovi()
        lista = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, svi_letovi["aa44"]["sifra_polazisnog_aerodroma"], svi_letovi["aa44"]["sifra_odredisnog_aerodorma"])
        self.assertIsNotNone(lista, msg="Nije vraćena kolekcija letova")
        self.assertTrue(len(lista)<=10, msg="Ima previse elemenata liste")
        self.assertDictEqual(
            svi_letovi["aa44"],
            lista[0],
            msg="Vrednosti od leta nisu dobre"
        )
    def test_trazenje_10_najjeftinijih_letova_neuspesno_nepostojeci_letovi(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: letovi"):
            lista = letovi.trazenje_10_najjeftinijih_letova(None, None, None)

    #--------------------------------------------------------------
    def test_izmena_letova_uspesna(self):
        pocetak_operativnosti = rand_datetime()
        kraj_operativnosti = pocetak_operativnosti + timedelta(days=10)
        nov_let = {
            "broj_leta": self.pun_let["broj_leta"],
            "sifra_polazisnog_aerodroma": rand_str(3),
            "sifra_odredisnog_aerodorma": rand_str(3),
            "vreme_poletanja": rand_time_str(),
            "vreme_sletanja": rand_time_str(),
            "sletanje_sutra": True,
            "prevoznik": rand_str(5),
            "dani": [konstante.SUBOTA, konstante.PONEDELJAK],
            "model": self.modeli_aviona[124],
            "cena": 100 + random.random() * 200,
            "datum_pocetka_operativnosti": pocetak_operativnosti,
            "datum_kraja_operativnosti": kraj_operativnosti,
        }
        svi_letovi = letovi.izmena_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            self.pun_let["broj_leta"],
            nov_let["sifra_polazisnog_aerodroma"],
            nov_let["sifra_odredisnog_aerodorma"],
            nov_let["vreme_poletanja"],
            nov_let["vreme_sletanja"],
            nov_let["sletanje_sutra"],
            nov_let["prevoznik"],
            nov_let["dani"],
            nov_let["model"],
            nov_let["cena"],
            nov_let["datum_pocetka_operativnosti"],
            nov_let["datum_kraja_operativnosti"]
        )
        self.assertIsNotNone(svi_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], svi_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            nov_let,
            svi_letovi[nov_let["broj_leta"]],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_izmena_letova_neuspesna(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: polaziste"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                rand_str(7),
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_izmena_letova_neuspesna_nepostojeci_let(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: nepostojeci let"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                rand_str(7),
                rand_str(7),
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_izmena_letova_neuspesna_polaziste(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: polaziste"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                rand_str(7),
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_izmena_letova_neuspesna_odrediste(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: odrediste"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                rand_str(7),
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_izmena_letova_neuspesna_vreme_poletanja(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: vreme leta"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                rand_str(7),
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_izmena_letova_neuspesna_vreme_sletanja(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: vreme sletanja"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                rand_str(7),
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_izmena_letova_neuspesna_sletanje_sutra(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: sletanje sutra"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                None,
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_izmena_letova_neuspesna_prevoznik(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost:prevoznik"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                "",
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_izmena_letova_neuspesna_dani(self):
        with self.assertRaises(Exception, msg=Exception):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                [],
                self.pun_let["model"],
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )


    def test_izmena_letova_neuspesna_model(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: model"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodorma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                {},
                self.pun_let["cena"],
                self.pun_let["datum_pocetka_operativnosti"],
                self.pun_let["datum_kraja_operativnosti"]
            )

    def test_izmena_letova_pocetak_posle_kraja(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: pocetak posle kraja"):
            rezultat = letovi.izmena_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"],
                # Promenjen redosled
                self.pun_let["datum_kraja_operativnosti"],
                self.pun_let["datum_pocetka_operativnosti"]
            )

    def testiraj_letovi_fajl(self):
        let2 = copy.deepcopy(self.pun_let)
        let2["broj_leta"]="aa34"
        let2["sifra_polazisnog_aerodroma"]="TYO"
        let3 = copy.deepcopy(self.pun_let)
        let3["broj_leta"] = "aa35"
        let3["sifra_odredisnog_aerodorma"] = "TYO"
        referentni_letovi = {
            self.pun_let["broj_leta"]: self.pun_let,
            let2["broj_leta"]: let2,
            let3["broj_leta"]: let3
        }
        letovi.sacuvaj_letove(self.putanja, "|", referentni_letovi)

        ucitani_letovi = letovi.ucitaj_letove_iz_fajla(self.putanja, "|")
        self.assertIsNotNone(ucitani_letovi, msg="Nisu učitani letovi iz fajla")
        self.assertEqual(len(referentni_letovi), len(ucitani_letovi), msg="Dužine učitanih letova nisu jednake")
        for k in ucitani_letovi:

            print(k)
            ucitani_let = ucitani_letovi[k]
            print(ucitani_let["sifra_odredisnog_aerodorma"])
            self.assertEqual(referentni_letovi[k]["broj_leta"],
                             ucitani_let["broj_leta"], msg="Učitani letovi se ne poklapaju broj leta")
            self.assertEqual(referentni_letovi[k]["sifra_polazisnog_aerodroma"], ucitani_let["sifra_polazisnog_aerodroma"],msg="Učitani letovi se ne poklapaju polaziste")
            self.assertEqual(referentni_letovi[k]["sifra_odredisnog_aerodorma"],
                             ucitani_let["sifra_odredisnog_aerodorma"], msg="Učitani letovi se ne poklapaju odrediste")
            self.assertEqual(referentni_letovi[k]["vreme_poletanja"],
                             ucitani_let["vreme_poletanja"], msg="Učitani letovi se ne poklapaju vreme_poletanja")
            self.assertEqual(referentni_letovi[k]["vreme_sletanja"],
                             ucitani_let["vreme_sletanja"], msg="Učitani letovi se ne poklapaju vreme_sletanja")
            self.assertEqual(referentni_letovi[k]["sletanje_sutra"],
                             ucitani_let["sletanje_sutra"], msg="Učitani letovi se ne poklapaju sletanje sletanje_sutra")
            self.assertEqual(referentni_letovi[k]["prevoznik"],
                             ucitani_let["prevoznik"],
                             msg="Učitani letovi se ne poklapaju sletanje prevoznik")
            self.assertEqual(referentni_letovi[k]["cena"],
                             ucitani_let["cena"],
                             msg="Učitani letovi se ne poklapaju sletanje cena")

            #self.assertDictEqual(referentni_letovi[k], ucitani_let, msg="Učitani letovi se ne poklapaju")


    def get_letovi(self):
        let1 = copy.deepcopy(self.pun_let)
        let1["cena"] = 0.1
        let1["broj_leta"] = "aa44"

        let2 = copy.deepcopy(self.pun_let)
        let2["cena"] = 100 + random.random() * 200
        let2["broj_leta"] = rand_str(2) + str(randint(50,99))

        let3 = copy.deepcopy(self.pun_let)
        let3["cena"] = 100 + random.random() * 200
        let3["broj_leta"] = rand_str(2) + str(randint(50,99))

        let13 = copy.deepcopy(self.pun_let)
        let13["cena"] = 100 + random.random() * 200
        let13["broj_leta"] = rand_str(2) + str(randint(50,99))

        let4 = copy.deepcopy(self.pun_let)
        let4["cena"] = 100 + random.random() * 200
        let4["broj_leta"] = rand_str(2) + str(randint(50,99))

        let4 = copy.deepcopy(self.pun_let)
        let4["cena"] = 100 + random.random() * 200
        let4["broj_leta"] = rand_str(2) + str(randint(50,99))

        let5 = copy.deepcopy(self.pun_let)
        let5["cena"] = 100 + random.random() * 200
        let5["broj_leta"] = rand_str(2) + str(randint(50,99))

        let6 = copy.deepcopy(self.pun_let)
        let6["cena"] = 100 + random.random() * 200
        let6["broj_leta"] = rand_str(2) + str(randint(50,99))

        let7 = copy.deepcopy(self.pun_let)
        let7["cena"] = 100 + random.random() * 200
        let7["broj_leta"] = rand_str(2) + str(randint(50,99))

        let8 = copy.deepcopy(self.pun_let)
        let8["cena"] = 100 + random.random() * 200
        let8["broj_leta"] = rand_str(2) + str(randint(50,99))

        let9 = copy.deepcopy(self.pun_let)
        let9["cena"] = 100 + random.random() * 200
        let9["broj_leta"] = rand_str(2) + str(randint(50,99))

        let10 = copy.deepcopy(self.pun_let)
        let10["cena"] = 100 + random.random() * 200
        let10["broj_leta"] = rand_str(2) + str(randint(50,99))
        svi_letovi = {self.pun_let["broj_leta"]: self.pun_let,
                      let1["broj_leta"]: let1,
                      let2["broj_leta"]: let2,
                      let3["broj_leta"]: let3,
                      let4["broj_leta"]: let4,
                      let5["broj_leta"]: let5,
                      let6["broj_leta"]: let6,
                      let7["broj_leta"]: let7,
                      let8["broj_leta"]: let8,
                      let9["broj_leta"]: let9,
                      let10["broj_leta"]: let10,
                      let13["broj_leta"]: let13}
        return svi_letovi

    def test_checkin_validan(self):
        konkretni_let = {
            "sifra": 1234,
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska": rand_datetime(start=datetime.now() + timedelta(hours=96)),
            "datum_i_vreme_dolaska": rand_datetime(start=datetime.now() + timedelta(hours=100))
        }
        letovi.podesi_matricu_zauzetosti(self.svi_letovi, konkretni_let)
        model_aviona = self.pun_let["model"]
        red = random.randint(1, model_aviona["broj_redova"])
        pozicija_index = random.randint(0, len(model_aviona["pozicije_sedista"])-1)
        pozicija = model_aviona["pozicije_sedista"][pozicija_index]
        # dummy karta kojoj očekujemo da samo bude postavljena pozicija sedišta
        karta = {}
        konkretni_let, karta = letovi.checkin(karta, self.svi_letovi, konkretni_let, red, pozicija)
        zauzetost = letovi.matrica_zauzetosti(konkretni_let)
        self.assertTrue(zauzetost[red-1][pozicija_index])
        self.assertIn("sediste", karta)
        self.assertEqual(f"{pozicija}{red}", karta["sediste"])

    def test_checkin_prosao_checkin(self):
        konkretni_let = {
            "sifra": 1234,
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska": rand_datetime(start=datetime.now(), end=datetime.now() + timedelta(hours=24)),
            "datum_i_vreme_dolaska": rand_datetime(start=datetime.now(), end=datetime.now() + timedelta(hours=30))
        }
        letovi.podesi_matricu_zauzetosti(self.svi_letovi, konkretni_let)
        model_aviona = self.pun_let["model"]
        red = random.randint(1, model_aviona["broj_redova"])
        pozicija_index = random.randint(0, len(model_aviona["pozicije_sedista"])-1)
        pozicija = model_aviona["pozicije_sedista"][pozicija_index]
        with self.assertRaises(Exception, msg=f"Provera za checkin koji je prošao"):
            letovi.checkin({}, self.svi_letovi, konkretni_let, red, pozicija)


    def test_checkin_zauzeto(self):
        konkretni_let = {
            "sifra": 1234,
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska": rand_datetime(start=datetime.now() + timedelta(days=96)),
            "datum_i_vreme_dolaska": rand_datetime(start=datetime.now() + timedelta(hours=100))
        }
        letovi.podesi_matricu_zauzetosti(self.svi_letovi, konkretni_let)
        model_aviona = self.pun_let["model"]
        red = random.randint(1, model_aviona["broj_redova"])
        pozicija_index = random.randint(0, len(model_aviona["pozicije_sedista"])-1)
        pozicija = model_aviona["pozicije_sedista"][pozicija_index]
        letovi.checkin({}, self.svi_letovi, konkretni_let, red, pozicija)
        zauzetost = letovi.matrica_zauzetosti(konkretni_let)
        self.assertTrue(zauzetost[red-1][pozicija_index])

        with self.assertRaises(Exception, msg=f"Provera za checkin zauzetog mesta"):
            letovi.checkin({}, self.svi_letovi, konkretni_let, red, pozicija)

    def test_checkin_nevalidna_pozicija(self):
        konkretni_let = {
            "sifra": 1234,
            "broj_leta": self.pun_let["broj_leta"],
            "datum_i_vreme_polaska": rand_datetime(start=datetime.now() + timedelta(hours=96)),
            "datum_i_vreme_dolaska": rand_datetime(start=datetime.now() + timedelta(hours=100))
        }
        letovi.podesi_matricu_zauzetosti(self.svi_letovi, konkretni_let)
        model_aviona = self.pun_let["model"]
        validni_red = random.randint(1, model_aviona["broj_redova"])
        pozicija_index = random.randint(0, len(model_aviona["pozicije_sedista"])-1)
        validna_pozicija = model_aviona["pozicije_sedista"][pozicija_index]

        with self.assertRaises(Exception, msg=f"Provera za checkin nevalidnog reda"):
            nevalidni_red = model_aviona["broj_redova"] + random.randint(1, 10)
            letovi.checkin({}, self.svi_letovi, konkretni_let, nevalidni_red, validna_pozicija)

        with self.assertRaises(Exception, msg=f"Provera za checkin nevalidne pozicije"):
            nevalidna_pozicija = chr(ord('A') + len(model_aviona["pozicije_sedista"]) + random.randint(1, 10))
            letovi.checkin({}, self.svi_letovi, konkretni_let, validni_red, nevalidna_pozicija)


    def test_povezani_letovi(self):
        referentni_let = {
                "broj_leta": rand_str(2) + str(randint(10, 99)),
                "sifra_polazisnog_aerodroma": rand_str(3),
                "sifra_odredisnog_aerodorma": rand_str(3),
                "vreme_poletanja": rand_time_str(),
                "vreme_sletanja": rand_time_str(),
        }
        povezani_let = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "sifra_polazisnog_aerodroma": referentni_let["sifra_odredisnog_aerodorma"],
            "sifra_odredisnog_aerodorma": rand_str(3),
            "vreme_poletanja": rand_time_str(),
            "vreme_sletanja": rand_time_str(),
        }

        nepovezani_let = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "sifra_polazisnog_aerodroma": povezani_let["sifra_odredisnog_aerodorma"],
            "sifra_odredisnog_aerodorma": rand_str(3),
            "vreme_poletanja": rand_time_str(),
            "vreme_sletanja": rand_time_str(),
        }


        svi_letovi = {
            referentni_let["broj_leta"]: referentni_let,
            povezani_let["broj_leta"]: povezani_let,
            nepovezani_let["broj_leta"]: nepovezani_let
        }

        referentni_konkretni_let = {
            "sifra": random.randint(1000, 10000),
            "broj_leta": referentni_let["broj_leta"],
            "datum_i_vreme_polaska": rand_datetime(start=datetime.now() + timedelta(minutes=96)),
            "datum_i_vreme_dolaska": rand_datetime(start=datetime.now() + timedelta(minutes=100))
        }

        povezani_konkretni_let = {
            "sifra": random.randint(1000, 10000),
            "broj_leta": povezani_let["broj_leta"],
            "datum_i_vreme_polaska": referentni_konkretni_let["datum_i_vreme_dolaska"] + timedelta(minutes=100),
            "datum_i_vreme_dolaska":  referentni_konkretni_let["datum_i_vreme_dolaska"] + timedelta(minutes=200)
        }

        povezani_konkretni_let_u_proslosti = {
            "sifra": random.randint(1000, 10000),
            "broj_leta": povezani_let["broj_leta"],
            "datum_i_vreme_polaska": referentni_konkretni_let["datum_i_vreme_dolaska"] - timedelta(minutes=100),
            "datum_i_vreme_dolaska": referentni_konkretni_let["datum_i_vreme_dolaska"] - timedelta(minutes=200)
        }

        nepovezani_konkretni_let_polaziste = {
            "sifra": random.randint(1000, 10000),
            "broj_leta": povezani_let["broj_leta"],
            "datum_i_vreme_polaska": referentni_konkretni_let["datum_i_vreme_dolaska"] + timedelta(minutes=200),
            "datum_i_vreme_dolaska": referentni_konkretni_let["datum_i_vreme_dolaska"] + timedelta(minutes=300)
        }

        nepovezani_konkretni_let_vreme = {
            "sifra": random.randint(1000, 10000),
            "broj_leta": povezani_let["broj_leta"],
            "datum_i_vreme_polaska": referentni_konkretni_let["datum_i_vreme_dolaska"] + timedelta(minutes=200),
            "datum_i_vreme_dolaska": referentni_konkretni_let["datum_i_vreme_dolaska"] + timedelta(minutes=300)
        }

        svi_konkretni_letovi = {
            referentni_konkretni_let["sifra"]: referentni_konkretni_let,
            povezani_konkretni_let["sifra"]: povezani_konkretni_let,
            nepovezani_konkretni_let_polaziste["sifra"]: nepovezani_konkretni_let_polaziste,
            nepovezani_konkretni_let_vreme["sifra"]: nepovezani_konkretni_let_vreme
        }

        ocekivani_povezani_letovi = [povezani_konkretni_let]

        povezani_letovi = letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, referentni_konkretni_let)
        self.assertEqual(ocekivani_povezani_letovi, povezani_letovi)


    def test_povezani_letovi_nepostojeci_let(self):
        referentni_let = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "sifra_polazisnog_aerodroma": rand_str(3),
            "sifra_odredisnog_aerodorma": rand_str(3),
            "vreme_poletanja": rand_time_str(),
            "vreme_sletanja": rand_time_str(),
        }

        with self.assertRaises(Exception, msg=f"Povezani letovi za nepostojeći let"):
            letovi.povezani_letovi({}, {referentni_let["broj_leta"]: referentni_let}, referentni_let)


    def test_pregled_nerealizoivanih_letova(self):
        ocekivani_let = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "datum_pocetka_operativnosti": datetime.now() + timedelta(hours=random.randint(1, 100))
        }
        neocekivani_let_1 = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "datum_pocetka_operativnosti": datetime.now() - timedelta(hours=random.randint(1, 100))
        }
        neocekivani_let_2 = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "datum_pocetka_operativnosti": datetime.now() - timedelta(hours=random.randint(1, 100))
        }
        svi_letovi = {
            neocekivani_let_1["broj_leta"]: neocekivani_let_1,
            ocekivani_let["broj_leta"]: ocekivani_let,
            neocekivani_let_2["broj_leta"]: neocekivani_let_2
        }
        ocekivani_letovi = [ocekivani_let]
        nerealizovani_letovi = letovi.pregled_nerealizoivanih_letova(svi_letovi)
        self.assertListEqual(ocekivani_letovi, nerealizovani_letovi)


    def test_fleksibilni_letovi(self):
        ocekivani_let = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "datum_pocetka_operativnosti": datetime.now() + timedelta(hours=random.randint(1, 100)),
            "sifra_polazisnog_aerodroma": rand_str(3),
            "sifra_odredisnog_aerodorma": rand_str(3)

        }
        neocekivani_let_1 = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "datum_pocetka_operativnosti": datetime.now() - timedelta(hours=random.randint(1, 100)),
            "sifra_polazisnog_aerodroma": rand_str(3),
            "sifra_odredisnog_aerodorma": rand_str(3)
        }
        svi_letovi = {
            neocekivani_let_1["broj_leta"]: neocekivani_let_1,
            ocekivani_let["broj_leta"]: ocekivani_let
        }
        ocekivani_k_let = copy.deepcopy(self.konkretan_let)
        ocekivani_k_let["broj_leta"]= ocekivani_let["broj_leta"]
        ocekivani_letovi = [ocekivani_k_let]
        konkretni_letovi = letovi.fleksibilni_polasci(
            svi_letovi,
            {ocekivani_k_let["sifra"]: ocekivani_k_let},
            ocekivani_let["sifra_polazisnog_aerodroma"],
            ocekivani_let["sifra_odredisnog_aerodorma"],
            ocekivani_k_let["datum_i_vreme_polaska"],
            3,
            ocekivani_k_let["datum_i_vreme_dolaska"],)
        self.assertListEqual(ocekivani_letovi, konkretni_letovi)


    def test_fleksibilni_letovi_neuspesno(self):
        ocekivani_let = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "datum_pocetka_operativnosti": datetime.now() + timedelta(hours=random.randint(1, 100)),
            "sifra_polazisnog_aerodroma": rand_str(3),
            "sifra_odredisnog_aerodorma": rand_str(3)

        }
        neocekivani_let_1 = {
            "broj_leta": rand_str(2) + str(randint(10, 99)),
            "datum_pocetka_operativnosti": datetime.now() - timedelta(hours=random.randint(1, 100)),
            "sifra_polazisnog_aerodroma": rand_str(3),
            "sifra_odredisnog_aerodorma": rand_str(3)
        }
        svi_letovi = {
            neocekivani_let_1["broj_leta"]: neocekivani_let_1,
            ocekivani_let["broj_leta"]: ocekivani_let
        }
        ocekivani_letovi = []
        konkretni_letovi = letovi.fleksibilni_polasci(
            svi_letovi,
            {self.konkretan_let["sifra"]: self.konkretan_let},
            ocekivani_let["sifra_polazisnog_aerodroma"],
            ocekivani_let["sifra_odredisnog_aerodorma"],
            self.konkretan_let["datum_i_vreme_polaska"],
            3,
            self.konkretan_let["datum_i_vreme_dolaska"],)
        self.assertListEqual(ocekivani_letovi, konkretni_letovi)

if __name__ == '__main__':
    unittest.main()

