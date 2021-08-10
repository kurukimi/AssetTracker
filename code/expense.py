from decimal import Decimal


class Expense:
    def __init__(self, name=None, value=None, date=None):
        """Expense-luokka: kuvaa jokaista
         ostotapahtumaa (sama kohde voi esiintyä useamman kerran)"""
        self.name = name
        self.value = Decimal(value)
        self.date = date

    def get_value(self):
        return self.value

    def get_date(self):
        return self.date

    def get_name(self):
        return self.name


