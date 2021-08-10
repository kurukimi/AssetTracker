from allexpenses import allExpenses
from decimal import Decimal
import datetime

class Dataread:
    def __init__(self):
        """Dataread-luokan tarkoitus on lukea tiedosto, ja lisätä siitä saatu data ostotapahtumiin (expense)"""
        self.data = []
        self.file = None
        self.files = []
        self.expenses = allExpenses()


    def get_expenses(self):
        return self.expenses

    def get_data(self):
        return self.data

    def add_file(self, name):
        # Lisää tiedostonimen muuttujaan ja aloittaa funktiot
        self.file = name
        self.parse_income()
        self.files.append(self.file)
        self.sort_expenses()

    def parse_income(self):
        # Jaottelee datasta rivit joiden rahasumma alkaa miinuksella, eli jotka on menoja
        temp = []
        with open(self.file, 'r') as filu:
            filu.seek(0)
            first = filu.read(1)
            if not first:
                raise IndexError
            filu.seek(0)
            for line in filu:
                if line.split(';')[2].startswith('-'):
                    temp.append(line.strip('\n'))
        self.data = temp


    def sort_expenses(self):
        # jaottelee meno-riveistä eri kohdat: nimet, päivämäärät, arvot ja lisää ne expenses olioon
        # add_expenses funktiolla
        for line in self.data:
            value = line.split(';')[2]
            date = line.split(';')[1]
            name = line.split(';')[5].strip('"')
            # tarkastetaan, että value ja date on oikeaa muotoa, muuten nostetaan errori
            try:
                float(value.strip('-').replace(',', '.'))
                ints = date.split('.')
                if len(ints) != 3:
                    raise ValueError
                datetime.datetime.strptime(date, "%d.%m.%Y")
            except ValueError:
                raise ValueError
            self.expenses.add_expense(name, Decimal(value.strip('-').replace(',', '.')), date)
        if len(self.files) < 2:
            self.expenses.set_to_plot(self.expenses.get_expenseobjs())
        self.expenses.update_category()





