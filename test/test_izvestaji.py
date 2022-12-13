import os
import unittest
import copy
import random

from common import konstante
from izvestaji import izvestaji
from test.test_utils import rand_str, rand_valid_user, gen_rand_valid_users
import random
import string
from datetime import date

class IzvestajiTest(unittest.TestCase):
    def setUp(self):
        self.modeli_aviona = {
            123: {"id": 123, "naziv": "Boeing747", "broj_redova": 44, "pozicija_sedista": "A"},
            124: {"id": 124, "naziv": "Boeing748", "broj_redova": 45, "pozicija_sedista": "B"}
        }
        self.pun_let = {
            "broj_leta": "aa33",
            "sifra_polazisnog_aerodroma": "BJS",
            # pitanje, da li je u redu da stavim ovako nazive, ili nekako drugacije?
            "sifra_odredisnog_aerodorma": "LON",
            "vreme_poletanja": "13:34",  # pitanje, da li je u redu da stavim ovako vreme, ili nekako drugacije?
            "vreme_sletanja": "14:50",
            "sletanje_sutra": False,
            "prevoznik": "prevoznik1",
            "dani": [konstante.CETVRTAK, konstante.NEDELJA],
            "model": self.modeli_aviona[123],
            "cena": 200
        }

        self.konkretan_let = {
            "sifra": 1234,
            "broj_leta":"aa33",
            "datum_polaska" : "07.01.2023.",
            "datum_dolaska": "07.01.2023."
        }

        self.puna_karta = {
            "broj_karte": 1,
            "sifra_leta": "aa33", #sifra konkretnog leta
            "sifra_konkretnog_leta":1234,
            "kupac": ''.join(random.sample(string.ascii_lowercase, 6)),
            "prodavac": ''.join(random.sample(string.ascii_lowercase, 7)),
            "sifra_sedista": "b3",
            "datum_prodaje" : "03.12.2022.",
            "obrisana": False
        }

        self.putanja = "test_karte.csv"

        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_uspesan_izvestaj_prodatih_karata_za_dan_prodaje(self):
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"]= 2
        karta1["datum_prodaje"] = "4.12.2022."
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["broj_karte"] = 3
        sve_karte = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(
            { self.puna_karta["broj_karte"]:self.puna_karta,
              karta1["broj_karte"]: karta1,
              karta2["broj_karte"]: karta2
             },
            self.puna_karta["dan_prodaje"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(karta1, sve_karte, msg="Karta je u kolekciji")
        self.assertIn(karta2, sve_karte, msg="Karta je u kolekciji")
        self.assertEqual(2, len(sve_karte), msg="Sve karte su tu")

    def test_neuspesan_izvestaj_prodatih_karata_za_dan_prodaje(self):
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"]= 2
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["broj_karte"] = 3

        sve_karte = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(
            {self.puna_karta["broj_karte"]:self.puna_karta,
             karta1["broj_karte"]:karta1,
             karta2["broj_karte"]:karta2 },
            "28.09.2022." #da li mozda neki bolji nacin za datume da uzmem?
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertEqual(0, len(sve_karte), msg="Nema karata")

    def test_izvestaj_prodatih_karata_za_dan_polaska(self):
        konkretan_let1 = copy.deepcopy(self.konkretan_let)
        konkretan_let1["sifra"] =1235
        konkretan_let1["datum_polaska"] = "08.09.2023."

        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2

        karta2 = copy.deepcopy(self.puna_karta)
        karta2["broj_karte"] = 3
        karta2["sifra_konkretnogg_leta"] = 1235

        svi_konkretni_letovi={
            self.konkretan_let["sifra"]: self.konkretan_let,
            konkretan_let1["sifra"]: konkretan_let1
        }
        sve_karte = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            svi_konkretni_letovi,
            self.konkretan_let["datum_polaska"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(karta1, sve_karte, msg="Karta je u kolekciji")
        self.assertIn(karta2, sve_karte, msg="Karta je u kolekciji")
        self.assertEqual(2, len(sve_karte), msg="Sve karte su tu")

    def test_neuspesan_izvestaj_prodatih_karata_za_dan_polaska(self):
        konkretan_let1 = copy.deepcopy(self.konkretan_let)
        konkretan_let1["sifra"] = 1235
        konkretan_let1["datum_polaska"] = "08.09.2023."

        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"]= 2

        karta2 = copy.deepcopy(self.puna_karta)
        karta2["broj_karte"] = 3
        karta2["sifra_konkretnogg_leta"] =1235

        svi_konkretni_letovi = {
            self.konkretan_let["sifra"]: self.konkretan_let,
            konkretan_let1["sifra"]: konkretan_let1
        }
        sve_karte = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(
            {self.puna_karta["broj_karte"]:self.puna_karta,
             karta1["broj_karte"]:karta1,
             karta2["broj_karte"]:karta2 },
            svi_konkretni_letovi,
            "29.01.2023."
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertEqual(0, len(sve_karte), msg="Nema karata")

    def test_izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(self):
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2
        karta1["datum_prodaje"] = "03.04.2022."
        karta1["prodavac"] =''.join(random.sample(string.ascii_lowercase, 7)),
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_prodaje"] = "03.04.2022."
        karta2["broj_karte"] = 3

        sve_karte = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            "03.12.2022.",
            self.puna_karta["prodavac"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertEqual(1, len(sve_karte), msg="Nema karata")

    def test_neuspesan_izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(self):
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2
        karta1["datum_polaska"] = "neki"
        karta1["prodavac"] = ''.join(random.sample(string.ascii_lowercase, 7)),
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_polaska"] = karta1["prodavac"]
        karta2["broj_karte"] = 3

        sve_karte = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            "05.05.2022.",
            ''.join(random.sample(string.ascii_lowercase, 8)),
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertEqual(0, len(sve_karte), msg="Nema karata")


    def test_izvestaj_ubc_prodatih_karata_za_dan_prodaje(self):
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2
        karta1["datum_prodaje"] = "03.04.2022."
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_polaska"] = "03.04.2022."
        karta2["broj_karte"] = 3

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            karta1["datum_prodaje"]
        )
        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat), msg="")
        self.assertNotEqual(0, rezultat[0], msg="")
        self.assertNotEqual(0, rezultat[0], msg="")

    def test_izvestaj_ubc_prodatih_karata_za_dan_prodaje_nepostojeci_dan(self):
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2
        karta1["datum_polaska"] = "03.04.2022."
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_polaska"] = "03.04.2022."
        karta2["broj_karte"] = 3

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            "07.07.2022."
        )
        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(0, len(rezultat), msg="")
        self.assertNotEqual(0, rezultat[0], msg="")
        self.assertNotEqual(0, rezultat[0], msg="")

    def test_izvestaj_ubc_prodatih_karata_za_dan_polaska(self):
        konkretan_let1 = copy.deepcopy(self.konkretan_let)
        konkretan_let1["sifra"] = 1235
        konkretan_let1["datum_polaska"] = "08.09.2023."

        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2

        karta2 = copy.deepcopy(self.puna_karta)
        karta2["broj_karte"] = 3
        karta2["sifra_konkretnogg_leta"] = 1235
        karta1["sifra_konkretnogg_leta"] = 1235

        svi_konkretni_letovi = {
            self.konkretan_let["sifra"]: self.konkretan_let,
            konkretan_let1["sifra"]: konkretan_let1
        }

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            svi_konkretni_letovi,
            "08.09.2023."
        )
        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat), msg="")
        self.assertNotEqual(0, rezultat[0], msg="")
        self.assertNotEqual(0, rezultat[0], msg="")

    def test_neuspesan_izvestaj_ubc_prodatih_karata_za_dan_polaska(self):
        konkretan_let1 = copy.deepcopy(self.konkretan_let)
        konkretan_let1["sifra"] = 1235
        konkretan_let1["datum_polaska"] = "08.09.2023."

        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2

        karta2 = copy.deepcopy(self.puna_karta)
        karta2["broj_karte"] = 3
        karta2["sifra_konkretnogg_leta"] = 1235

        svi_konkretni_letovi = {
            self.konkretan_let["sifra"]: self.konkretan_let,
            konkretan_let1["sifra"]: konkretan_let1
        }

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            svi_konkretni_letovi,
            "17.03.2022."
        )
        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat), msg="")
        self.assertNotEqual(0, rezultat[0], msg="")
        self.assertNotEqual(0, rezultat[0], msg="")


    def test_izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(self):
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2
        karta1["datum_prodaje"] = "08.09.2022."
        karta1["prodavac"] = ''.join(random.sample(string.ascii_lowercase, 7)),
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_prodaje"] = "08.09.2022."
        karta2["prodavac"] = karta1["prodavac"]
        karta2["broj_karte"] = 3

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2},
            "08.09.2022.",
            karta1["prodavac"]
        )
        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat), msg="")
        self.assertNotEqual(0, rezultat[0], msg="")
        self.assertNotEqual(0, rezultat[0], msg="")


    def test_izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(self):
        today = date.today()
        karta1 = copy.deepcopy(self.puna_karta)
        karta1["broj_karte"] = 2
        karta1["datum_prodaje"] = today.strftime("%d.%m.%Y.")
        karta1["prodavac"] = ''.join(random.sample(string.ascii_lowercase, 7)),
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["datum_prodaje"] = today.strftime("%d.%m.%Y.")
        karta2["broj_karte"] = 3

        self.puna_karta["datum_prodaje"] = today.strftime("%d.%m.%Y.")

        rezultat = izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(
            {self.puna_karta["broj_karte"]: self.puna_karta,
             karta1["broj_karte"]: karta1,
             karta2["broj_karte"]: karta2})

        self.assertIsNotNone(rezultat, msg="Nije vraćena kolekcija ")
        self.assertEqual(2, len(rezultat), msg="")