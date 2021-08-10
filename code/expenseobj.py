from decimal import Decimal


class Expenseobj:
    def __init__(self, name):
        """Expenseobj-luokka kuvaa kuluja -eri- kohteisiin. samaan kohteeseen laskettu yhteen.
         (vrt. Expense-luokka: kuvaa jokaista
         ostotapahtumaa (sama kohde voi esiintyä useamman kerran)"""
        # Funktioiden nimet itsessään kuvaavat ainakin toistaiseksi tarpeeksi niiden toimintaa
        self.name = name
        self.value = Decimal(0.0)
        self.dates = []
        self.category = None
        self.importance = 0

    def in_category(self, category, bool=False):
        # kun Expenses luokassa luodaan kategoria, liitetään se Expenseobj:n tällä funktiolla
        if bool:
            self.category = category
        else:
            self.category = None

    def get_category(self):
        return self.category

    def add_value(self, value):
        self.value += Decimal(value)

    def add_date(self, date):
        self.dates.append(date)

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_date(self):
        return self.dates

    def increase_importance(self, points):
        # pisteenlaskua säästöä varten
        self.importance += points

    def decrease_importance(self, points):
        self.importance -= points

    def clear_importance(self):
        self.importance = 0

    def get_importance(self):
        return self.importance