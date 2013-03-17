"""Bank accounts class"""


import datetime


class BankaError(Exception):
    pass


class NotPositiveError(BankaError):
    pass


class NotActiveError(BankaError):
    pass


class NotInactiveError(BankaError):
    pass


class BadFormatError(BankaError):
    pass


class NotCoveredPickError(BankaError):
    pass


class BankovniUcet:
    def __init__(self, jmeno_zakaznika, aktualni_vyse_uspor=0, rocni_urok=0,
                 datum_zalozeni=datetime.date.today(), stav_uctu="aktivni"):
        """Initialize new instance passing customer name (required), saved
           money, annual rate, creation date and account status."""
        self.jmeno_zakaznika = jmeno_zakaznika
        self.aktualni_vyse_uspor = aktualni_vyse_uspor
        self.rocni_urok = rocni_urok
        self.datum_zalozeni = datum_zalozeni
        self.stav_uctu = stav_uctu

    def deaktivovat(self):
        """Lock account. No transactions are possible."""
        # Testing wheather account is unlocked and locking it.
        if self.je_zamcen():
            raise NotActiveError("Deaktivovat lze jen aktivni ucty.")
        self.stav_uctu = "neaktivni"

    def aktivovat(self):
        """Unlock account. Transactions are possible."""
        # Testing wheather account is locked and unlocking it.
        if not self.je_zamcen():
            raise NotInactiveError("Aktivovat lze jen neaktivni ucty.")
        self.stav_uctu = "aktivni"

    def vlozit(self, castka):
        """Deposit money passing the amount."""
        # Test whether the account is unlocked.
        if self.je_zamcen():
            raise NotActiveError("Vkladat lze jen na aktivni ucty.")
        # Test whether amount is number in correct format.
        if not isinstance(castka, int) and not isinstance(castka, float):
            raise BadFormatError("Spatny format castky. Lze zadavat cislice " \
                                 "bez mezer, nezacinajici nulou, desetinnou " \
                                 "carku zapsat teckou.")
        # Test whether amount is positive.
        if castka <= 0:
            raise NotPositiveError("Na ucet lze vkladat jen kladne castky.")
        # Depositing money.
        self.aktualni_vyse_uspor += castka

    def vybrat(self, castka):
        """Withdraw money from account passing the amount."""
        # Test whether the account is unlocked.
        if self.je_zamcen():
            raise NotActiveError("Vybirat lze jen z aktivnich uctu.")
        # Test whether amount is number in correct format.
        if not isinstance(castka, int) and not isinstance(castka, float):
            raise BadFormatError("Spatny format castky. Lze zadavat cislice " \
                                 "bez mezer, nezacinajici nulou, desetinnou " \
                                 "carku zapsat teckou.")
        # Test whether amount is positive.
        if castka <= 0:
            raise NotPositiveError("Z uctu lze vybirat jen kladne castky.")
        # Test whether account is uncovered.
        if castka > self.ekvivalentni_zustatek():
            raise NotCoveredPickError("Pozadavek na vyber je vetsi nez " \
                                      "prostredky dostupne na uctu.")
        # Withdrawing money.
        self.aktualni_vyse_uspor -= castka

    def vypis(self):
        """Print all the information about account with stored data."""
        print "Jmeno:", self.jmeno_zakaznika
        print "Zustatek:", self.aktualni_vyse_uspor
        print "Rocni urokova sazba:", self.rocni_urok
        print "Datum zalozeni:", self.datum_zalozeni
        print "Stav uctu:", self.stav_uctu

    def ekvivalentni_zustatek(self):
        """Returns the sum of saved money."""
        return self.aktualni_vyse_uspor

    def je_zamcen(self):
        """Returns true when account is locked."""
        if self.stav_uctu == 'aktivni':
            return False
        else:
            return True
