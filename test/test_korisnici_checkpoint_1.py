import copy
import os
import random
import unittest

from korisnici import korisnici
from test.test_utils import rand_str, rand_valid_user


class KorisnikTest(unittest.TestCase):
    def setUp(self):
        self.pun_korisnik = rand_valid_user()
        self.putanja = "test_korisnici.csv"
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_kreiraj_prazni(self):
        # Prodji kroz sve kljuceve, postavi jedan na None, pa pozovi funkciju
        for key in self.pun_korisnik:
            korisnik = copy.deepcopy(self.pun_korisnik)
            korisnik[key] = None
            rezultat = korisnici.kreiraj_korisnika(
                {},
                False,  # azuriraj
                korisnik["uloga"],
                korisnik["korisnicko_ime"],
                korisnik["lozinka"],
                korisnik["ime"],
                korisnik["prezime"],
                korisnik["email"],
                korisnik["pasos"],
                korisnik["drzavljanstvo"],
                korisnik["telefon"],
                korisnik["pol"])
            self.assertTrue(type(rezultat) is str, msg=f"Provera za nedostajucu vrednost: {key}")
            self.assertTrue(len(rezultat)>0, msg=f"Provera za nedostajucu vrednost: {key}")

    def test_kreiraj_postojece_korisnicko_ime(self):
        svi_korisnici = {
            self.pun_korisnik["korisnicko_ime"]: self.pun_korisnik
        }
        rezultat = korisnici.kreiraj_korisnika(
            svi_korisnici,
            False,  # azuriraj
            self.pun_korisnik["uloga"],
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            self.pun_korisnik["email"],
            self.pun_korisnik["pasos"],
            self.pun_korisnik["drzavljanstvo"],
            self.pun_korisnik["telefon"],
            self.pun_korisnik["pol"])
        self.assertTrue(type(rezultat) is str, msg=f"Postojece korisnicko ime:")
        self.assertTrue(len(rezultat)>0, msg=f"Postojece korisnicko ime")

    def test_azuriraj_nepostojece_korisnicko_ime(self):
        svi_korisnici = {
            self.pun_korisnik["korisnicko_ime"]: self.pun_korisnik
        }
        rezultat = korisnici.kreiraj_korisnika(
            {},
            True,  # azuriraj
            self.pun_korisnik["uloga"],
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            self.pun_korisnik["email"],
            self.pun_korisnik["pasos"],
            self.pun_korisnik["drzavljanstvo"],
            self.pun_korisnik["telefon"],
            self.pun_korisnik["pol"])
        self.assertTrue(type(rezultat) is str, msg=f"Nepostojece korisnicko ime pri azuriranju")
        self.assertTrue(len(rezultat)>0, msg=f"Nepostojece korisnicko ime pri azuriranju")

    def test_email(self):
        rezultat = korisnici.kreiraj_korisnika(
            {},
            False,  # azuriraj
            self.pun_korisnik["uloga"],
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            "email_bez_at",
            self.pun_korisnik["pasos"],
            self.pun_korisnik["drzavljanstvo"],
            self.pun_korisnik["telefon"],
            self.pun_korisnik["pol"])

        self.assertTrue(type(rezultat) is str, msg=f"Email provera bez @")
        self.assertTrue(len(rezultat)>0, msg=f"Email provera bez @")

        rezultat = korisnici.kreiraj_korisnika(
            {},
            False,  # azuriraj
            self.pun_korisnik["uloga"],
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            "email@email.vise.poddomena",
            self.pun_korisnik["pasos"],
            self.pun_korisnik["drzavljanstvo"],
            self.pun_korisnik["telefon"],
            self.pun_korisnik["pol"])
        self.assertTrue(type(rezultat) is str, msg=f"Email provera sa @ ali sa više poddomena")
        self.assertTrue(len(rezultat)>0, msg=f"Email provera bez @")

    def test_pasos(self):
        rezultat = korisnici.kreiraj_korisnika(
            {},
            False,  # azuriraj
            self.pun_korisnik["uloga"],
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            self.pun_korisnik["email"],
            "abcdefghi",
            self.pun_korisnik["drzavljanstvo"],
            self.pun_korisnik["telefon"],
            self.pun_korisnik["pol"])

        self.assertTrue(type(rezultat) is str, msg=f"Pasoš nebrojevni string")
        self.assertTrue(len(rezultat)>0, msg=f"Pasoš nebrojevni string")

        rezultat = korisnici.kreiraj_korisnika(
            {},
            False,  # azuriraj
            self.pun_korisnik["uloga"],
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            self.pun_korisnik["email"],
            123,
            self.pun_korisnik["drzavljanstvo"],
            self.pun_korisnik["telefon"],
            self.pun_korisnik["pol"])

        self.assertTrue(type(rezultat) is str, msg=f"Pasoš manje od 9 cifara")
        self.assertTrue(len(rezultat)>0, msg=f"Pasoš manje od 9 cifara")

        rezultat = korisnici.kreiraj_korisnika(
            {},
            False,  # azuriraj
            self.pun_korisnik["uloga"],
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            self.pun_korisnik["email"],
            111111111111,
            self.pun_korisnik["drzavljanstvo"],
            self.pun_korisnik["telefon"],
            self.pun_korisnik["pol"])

        self.assertTrue(type(rezultat) is str, msg=f"Pasoš više od 9 cifara")
        self.assertTrue(len(rezultat)>0, msg=f"Pasoš više od 9 cifara")

    def test_broj_telefona(self):
        rezultat = korisnici.kreiraj_korisnika(
            {},
            False,  # azuriraj
            self.pun_korisnik["uloga"],
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            self.pun_korisnik["email"],
            self.pun_korisnik["pasos"],
            self.pun_korisnik["drzavljanstvo"],
            "abcdefghi",
            self.pun_korisnik["pol"])
        self.assertTrue(type(rezultat) is str, msg="Broj telefona nije validan")
        self.assertTrue(len(rezultat)>0, msg=f"Broj telefona nije validan")

    def test_uloga(self):
        rezultat = korisnici.kreiraj_korisnika(
            {},
            False,  # azuriraj
            "nepoznata_uloga",
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            self.pun_korisnik["email"],
            self.pun_korisnik["pasos"],
            self.pun_korisnik["drzavljanstvo"],
            self.pun_korisnik["telefon"],
            self.pun_korisnik["pol"])
        self.assertTrue(type(rezultat) is str, msg=f"Uloga nije validna")
        self.assertTrue(len(rezultat)>0, msg=f"Uloga nije validna")

    def testiraj_korisnici_fajl(self):
        referentni_korisnici = {}
        for i in range(10):
            korisnik = {key: rand_str(10) for key in self.pun_korisnik}
            korisnik["uloga"] = self.pun_korisnik["uloga"]
            korisnik["pasos"] = random.randint(100000001, 999999999)
            korisnik["telefon"] = random.randint(100000001, 999999999)
            korisnik["email"] += "@email.com"
            referentni_korisnici[korisnik["korisnicko_ime"]] = korisnik

        korisnici.sacuvaj_korisnike(self.putanja, "|", referentni_korisnici)

        ucitani_korisnici = korisnici.ucitaj_korisnike_iz_fajla(self.putanja, "|")
        self.assertEqual(len(referentni_korisnici), len(ucitani_korisnici))
        for korisnicko_ime in ucitani_korisnici:
            ucitani_korisnik = ucitani_korisnici[korisnicko_ime]
            self.assertDictEqual(referentni_korisnici[korisnicko_ime], ucitani_korisnik)

    def testiraj_login(self):
        korisnicko_ime = self.pun_korisnik["korisnicko_ime"]
        lozinka = self.pun_korisnik["lozinka"]
        svi_korisnici = {
            korisnicko_ime: self.pun_korisnik
        }

        rezultat = korisnici.login(svi_korisnici, "mika", "mikic")

        self.assertTrue(type(rezultat) is str, msg=f"Login nepostojeći")
        self.assertTrue(len(rezultat)>0, msg=f"Login nepostojeći")

        rezultat = korisnici.login(svi_korisnici, korisnicko_ime, "321")

        self.assertTrue(type(rezultat) is str, msg=f"Login pogrešna lozinka")
        self.assertTrue(len(rezultat)>0, msg=f"Login pogrešna lozinka")

        pronadjeni_korisnik = korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
        self.assertDictEqual(self.pun_korisnik, pronadjeni_korisnik, msg="Uspešan login")


if __name__ == '__main__':
    unittest.main()
