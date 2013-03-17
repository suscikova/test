"""Unit test for banka.py"""


import unittest
import random
import string
import banka


class VytvoreniUctu(unittest.TestCase):
    def setUp(self):
        # Sample of name values to be accepted.
        self.vzorek_jmen = ['j', 'JMENO', 'jmeno', 'jmeno prijmeni', "/jmeno/",
                            '', 'jmeno2', 'jmeno_prijmeni', '!@#$', '123456',
                            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']

    def test_zalozeni_uctu(self):
        """Creation of single account with default parameters."""
        for jmeno in self.vzorek_jmen:
            self.ucet = banka.BankovniUcet(jmeno)
            self.assertEqual(self.ucet.jmeno_zakaznika, jmeno)
            self.assertEqual(self.ucet.stav_uctu, "aktivni")

    def test_zalozeni_vice_uctu(self):
        """Creation of many accounts passing random names. The amount
        of accounts is random but less then 100"""
        hranice = random.randrange(1, 100, 1)  # random amnount of accounts
        for i in range(hranice):
            jmeno = ''.join(random.choice(string.ascii_letters + string.digits)
                            for x in range(random.randrange(1, 50, 1)))
            self.ucet = banka.BankovniUcet(jmeno)
            self.assertEqual(self.ucet.stav_uctu, "aktivni")


class MethodsCheck(unittest.TestCase):
    def setUp(self):
        # Simple account with default values.
        self.ucet = banka.BankovniUcet("Jmeno")
        # Locked account.
        self.novy_ucet = banka.BankovniUcet("Nove Jmeno",
                                            stav_uctu="neaktivni")
        # Accout with large amount of money.
        self.tucny_ucet = banka.BankovniUcet("Bohaty",
                                             aktualni_vyse_uspor=100000000)
        # Sample amount of money to be deposited or withdrawed.
        self.castky = [10000, 1500, 12.50, 49, 1000000]

    def test_Deaktivovat(self):
        # Test of deaktivovat() method. Account should be possible to lock.
        self.ucet.deaktivovat()
        self.assertEqual(self.ucet.je_zamcen(), True)

    def test_Aktivovat(self):
        # Test of aktivovat() method. Account should be possible to unlock.
        self.novy_ucet.aktivovat()
        self.assertEqual(self.novy_ucet.je_zamcen(), False)

    def test_Vlozit(self):
        # Test of vlozit() method. Saved money should increase in the deposited
        # money.
        for castka in self.castky:
            zustatek_pred_vlozenim = self.ucet.ekvivalentni_zustatek()
            self.ucet.vlozit(castka)
            self.assertEqual(zustatek_pred_vlozenim + castka,
                             self.ucet.ekvivalentni_zustatek())

    def test_Vybrat(self):
        # Test of vybrat() method. Saved money should decrease in the
        # withdrawed money.
        for castka in self.castky:
            zustatek_pred_vlozenim = self.tucny_ucet.ekvivalentni_zustatek()
            self.tucny_ucet.vybrat(castka)
            self.assertEqual(zustatek_pred_vlozenim - castka,
                             self.tucny_ucet.ekvivalentni_zustatek())

# Nevim jak otestovat metodu Vypis
#    def test_Vypis(self):
#        self.ucet.vypis()

    def test_EkvivalentniZustatek(self):
        # Test of ekvivalentni_zustatek() method. Method should return
        # nonnegative value.
        self.assertTrue(self.ucet.ekvivalentni_zustatek() >= 0)

    def test_JeZamcen(self):
        # Test of je_zamcen() method. Returns True/False if account is
        # locked/unlocked
        self.assertFalse(self.ucet.je_zamcen())
        self.assertTrue(self.novy_ucet.je_zamcen())


class ValidityCheck(unittest.TestCase):
    def setUp(self):
        # Sample amount of money to be deposited or withdrawed.
        self.seznam_castek = [1, 0.07843278, 1.5, 6.0000009, 1.0000000, 100,
                              34898, 123]
        # Simple account with default values.
        self.ucet = banka.BankovniUcet("Jmeno")
        # Locked account.
        self.novy_ucet = banka.BankovniUcet("Nove Jmeno",
                                             stav_uctu="neaktivni")
        # Accout with large amount of money.
        self.tucny_ucet = banka.BankovniUcet("Bohaty",
            aktualni_vyse_uspor=100000000)

    def test_ValidityVlozitVybrat(self):
        """The amount of saved money should not change when the same amount
        of money is deposited as withdrawed."""
        pocatecni_zustatek = self.ucet.ekvivalentni_zustatek()
        for castka in self.seznam_castek:
            self.ucet.vlozit(castka)
            zustatek_po_vlozeni = self.ucet.ekvivalentni_zustatek()
            self.assertNotEqual(pocatecni_zustatek, zustatek_po_vlozeni)
            self.ucet.vybrat(castka)
            zustatek_po_vyberu = self.ucet.ekvivalentni_zustatek()
            self.assertEqual(pocatecni_zustatek, zustatek_po_vyberu)

    def test_ValidityDeaktivovatAktivovat(self):
        """"Account "aktivni" status should not be changed after the account is
        deactivated and then activated."""
        stav = self.ucet.je_zamcen()
        self.ucet.deaktivovat()
        self.ucet.aktivovat()
        self.assertEqual(self.ucet.je_zamcen(), stav)

    def test_ValidityAktivovatDeaktivovat(self):
        """"Account "neaktivni" status should not be changed after the account
        is activated and then deactivated."""
        stav = self.novy_ucet.je_zamcen()
        self.novy_ucet.aktivovat()
        self.novy_ucet.deaktivovat()
        self.assertEqual(self.novy_ucet.je_zamcen(), stav)

    def test_PrevodPenez(self):
        """Money transfer between accounts should not lose any money."""
        for castka in self.seznam_castek:
            stav_zdroje_pred_prevodem = self.tucny_ucet.ekvivalentni_zustatek()
            stav_cile_po_prevodu = self.ucet.ekvivalentni_zustatek()
            self.tucny_ucet.vybrat(castka)
            self.ucet.vlozit(castka)
            # No money lose.
            self.assertEqual(stav_zdroje_pred_prevodem + stav_cile_po_prevodu,
                        self.tucny_ucet.ekvivalentni_zustatek() +
                        self.ucet.ekvivalentni_zustatek())
            # Nonzero amount should be transfered.
            self.assertNotEqual(stav_zdroje_pred_prevodem,
                        self.tucny_ucet.ekvivalentni_zustatek())
            # Correct amount of money should be transfered.
            self.assertEqual(stav_zdroje_pred_prevodem - castka,
                        self.tucny_ucet.ekvivalentni_zustatek())


class BadInputCheck(unittest.TestCase):
    def setUp(self):
        # Sample of bad expression of amount of money to be deposited
        # or withdrawed.
        self.slovni_castka = ["0008", "koruna", "12 korun", "2h", "3,50"]
        # Simple account with default values.
        self.ucet = banka.BankovniUcet("Jmeno")
        # Locked account.
        self.novy_ucet = banka.BankovniUcet("Nove Jmeno",
                                             stav_uctu="neaktivni")

    def test_VlozeniNekladneCastky(self):
        # vlozit() should fail for not positive amount of money.
        for s in (-1, 0):
            self.assertRaises(banka.NotPositiveError, self.ucet.vlozit, s)

    def test_VyberuNekladneCastky(self):
        # vybrat() should fail for not positive amount of money.
        for s in (-1, 0):
            self.assertRaises(banka.NotPositiveError, self.ucet.vybrat, s)

    def test_VlozeniNeciselneCastky(self):
        # vlozit() should fail for bad expression of amount of money.
        for s in self.slovni_castka:
            self.assertRaises(banka.BadFormatError, self.ucet.vlozit, s)

    def test_VyberuNeciselneCastky(self):
        # vybrat() should fail for bad expression of amount of money.
        for s in self.slovni_castka:
            self.assertRaises(banka.BadFormatError, self.ucet.vybrat, s)

    def test_AktivaceAktivniho(self):
        # aktivovat() should fail for unlocked account.
        self.assertRaises(banka.NotInactiveError, self.ucet.aktivovat)

    def test_DeaktivaceNeaktivniho(self):
        # deaktivovat() should fail for locked account.
        self.assertRaises(banka.NotActiveError, self.novy_ucet.deaktivovat)

    def test_VyberNekryteCastky(self):
        # vybrat() should fail when amount of withdrawed money is grater then
        # amount of saved money.
        self.ucet.vlozit(random.randrange(10000))
        for i in range(100):
            self.assertRaises(banka.NotCoveredPickError, self.ucet.vybrat,
                self.ucet.ekvivalentni_zustatek() + random.randrange(1, 100))

if __name__ == "__main__":
    unittest.main()
