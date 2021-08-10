from expenseobj import Expenseobj


class Expensecategory(Expenseobj):
    def __init__(self, name, expensesin):
        super(Expensecategory, self).__init__(name)
        """Expensecategory-luokka kuvaa käyttäjän luomaa kategoriaa kuluista (expenseobj)"""
        self.expensesIn = []
        self.set_expensesin(expensesin)
        self.value_calc()
        self.dates_calc()

    def value_calc(self):
        # lasketaan menojen yhteisarvo
        self.value = sum([expense.get_value() for expense in self.expensesIn])

    def dates_calc(self):
        # lasketaan kategoriaan kuuluvat päivämäärät yhteen listaan
        first = self.expensesIn[0].get_date()[:]
        for i in self.expensesIn[1:]:
            first.extend(i.get_date())
        self.dates = first

    def expenses_in(self):
        return self.expensesIn


    def add_expenses(self, expns):
        self.expensesIn.extend(expns)
        self.value_calc()

    def set_expensesin(self, expensesin):
        self.expensesIn = expensesin

