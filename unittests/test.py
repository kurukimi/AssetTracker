import unittest
import sys
sys.path.append('../rahan-seuranta-y2-2021')
sys.path.append('../code')
from dataread import Dataread
from allexpenses import allExpenses
from expenseobj import Expenseobj
from expense import Expense


class TestReadingData(unittest.TestCase):
    '''Testataan tiedostojen lukua'''
    '''Ei testata tiedoston lukemista muulla kun csv:llä, koska kaikki muut on jo poissuljettu 
    pyqt filedialogin avulla'''
    def test_add_invalid_file(self):
        with self.assertRaises(IndexError):
            Dataread().add_file('invalid_file.csv')

    def test_empty_file(self):
        with self.assertRaises(IndexError):
            Dataread().add_file('empty_file.csv')

    def test_valid_file(self):
        valid = Dataread()
        valid.add_file('valid_file.csv')
        self.assertEqual(len(valid.files), 1)   # Tiedosto on tallentunut
        valid_data =\
            ['01.02.2021;01.02.2021;-306,17;"106";TILISIIRTO;"Kauppa";FIXX YY HH;"";Viesti: testi   ;20210101',
            '01.02.2021;01.02.2021;-19,66;"162";PKORTTIMAKSU;"kirjakauppa";;"";Viesti:     OSTOPVM  210129 MF xyz VARMENTAJA 40 ;20210201',
            '01.02.2021;01.02.2021;-12,87;"162";PKORTTIMAKSU;"ruokakauppa";;"";Viesti:     OSTOPVM  210129 MF NRO xyz VARMENTAJA 4 ;20210201',
             '01.02.2021;01.02.2021;-4,99;"162";PKORTTIMAKSU;"Spotify";;"";Viesti:     OSTOPVM  210130 MF NRO xyz VARMENTAJA 05 ;20210201']
        self.assertEqual(valid.get_data(), valid_data)  # On luettu tiedostosta vain menot
        # Tarkastetaan, että tiedot luettu oikein expensesiin
        expense = valid.expenses.get_expenses()[2]
        self.assertEqual(expense.get_name(), "ruokakauppa")
        self.assertEqual(float(expense.get_value()), 12.87)
        self.assertEqual(expense.get_date(), '01.02.2021')

    def test_partially_valid_file(self):
        with self.assertRaises(ValueError):
            valid = Dataread()
            valid.add_file('partially_valid_file.csv')
        self.assertEqual(len(valid.files), 1)  # Tiedosto on tallentunut






class TestExpensesClass(unittest.TestCase):

    def test_add_expense(self):
        '''Testaa että luo expenset oikein ja lisätty listaan'''
        obj = allExpenses()
        obj.add_expense('kirjakauppa', 19.66, '02.02.2021')
        obj.add_expense('ruokakauppa', 12.87, '01.02.2021')
        expense_list = obj.get_expenses()
        self.assertEqual(expense_list[0].get_name(), 'kirjakauppa')
        self.assertEqual(expense_list[0].get_value(), 19.66)
        self.assertEqual(expense_list[0].get_date(), '02.02.2021')

        self.assertEqual(expense_list[1].get_name(), 'ruokakauppa')
        self.assertEqual(expense_list[1].get_value(), 12.87)
        self.assertEqual(expense_list[1].get_date(), '01.02.2021')


    def test_create_objects(self):
        '''Testaa että luodaan "kaupat" eli expenseobjt oikein, ja lisätään seriekseen oikein'''
        obj = allExpenses()
        obj.create_objects(Expense('kirjakauppa', 19.66, '02.02.2021'))
        obj.create_objects(Expense('ruokakauppa', 12.87, '01.02.2021'))
        # expenseobj listassa oikein
        self.assertEqual(obj.get_expenseobjs()[0].get_name(), 'kirjakauppa')
        self.assertEqual(float(obj.get_expenseobjs()[0].get_value()), 19.66)
        self.assertEqual(obj.get_expenseobjs()[0].get_date()[0], '02.02.2021')
        self.assertEqual(obj.get_expenseobjs()[1].get_name(), 'ruokakauppa')
        self.assertEqual(float(obj.get_expenseobjs()[1].get_value()), 12.87)
        self.assertEqual(obj.get_expenseobjs()[1].get_date()[0], '01.02.2021')
        # toplot listassa oikein
        self.assertEqual(obj.get_to_plot()[0].get_name(), 'kirjakauppa')
        self.assertEqual(float(obj.get_to_plot()[0].get_value()), 19.66)
        self.assertEqual(obj.get_to_plot()[0].get_date()[0], '02.02.2021')
        # serieksessä oikein
        self.assertEqual(obj.Series.series.slices()[0].label(), 'kirjakauppa')
        self.assertEqual(obj.Series.series.slices()[0].value(), 19.66)
        '''Testataan kun lisätään samanniminen kauppa, että se lisääntyy jo olemassaolevaan expenseobjhin'''
        obj.create_objects(Expense('kirjakauppa', 19.66, '02.02.2021'))
        self.assertEqual(len(obj.get_expenseobjs()), 2) # ei olla lisätty uutta objektia
        self.assertEqual(float(obj.get_expenseobjs()[0].get_value()), 19.66*2)  # samannimisen kaupan kulu on kasvanut
        self.assertEqual(obj.Series.series.slices()[0].value(), 19.66*2)    # kasvanut myös serieksessä
        self.assertEqual(float(obj.get_to_plot()[0].get_value()), 19.66 * 2) # ja toplotissa

    def test_adds_and_removes(self):
        '''Testataan pieniä add ja remove funktioita, joissa expenseobj tai lisätään toPlotiin'''
        obj = allExpenses()
        # Luodaan expenseobj
        expns = Expense('kirjakauppa', 19.66, '02.02.2021')
        obj.add_expenseobjs(expns)
        self.assertEqual(obj.get_expenseobjs()[0].get_name(), 'kirjakauppa')
        self.assertEqual(obj.get_expenseobjs()[0].get_value(), 19.66)
        # lisätään to plotiin, katsotaan että objekti menee listaan ja että lisätään myös seriesToplotiin
        obj.add_to_plot(expns)
        self.assertEqual(obj.get_to_plot()[0].get_name(), 'kirjakauppa')
        self.assertEqual(obj.get_to_plot()[0].get_value(), 19.66)
        self.assertEqual(obj.seriesDivided.series.slices()[0].label(), 'kirjakauppa')
        self.assertEqual(obj.seriesDivided.series.slices()[0].value(), 19.66)
        # poistetaan plotista
        obj.remove_from_plot(obj.get_expenseobjs()[0])
        self.assertEqual(len(obj.get_to_plot()), 0) # poistettu listasta, pituus 0
        self.assertEqual(len(obj.seriesDivided.series.slices()), 0)  # poistettu myös serieksestä


    def make_expnsobjs(self):
        '''apufunktio jossa luodaan expenseobjt'''
        obj = allExpenses()
        # luodaan ensin expenseobjt
        expnsobj = Expenseobj('kirjakauppa')
        expnsobj2 = Expenseobj('ruokakauppa')
        expnsobj.add_value(19.66)
        expnsobj.add_date('02.02.2021')
        expnsobj2.add_value(12.87)
        expnsobj2.add_date('01.02.2021')
        # lisätään listoihin
        obj.add_expenseobjs(expnsobj)
        obj.add_expenseobjs(expnsobj2)
        obj.add_to_plot(expnsobj)
        obj.add_to_plot(expnsobj2)
        return obj

    def make_ctgr(self):
        '''apufunktio jossa luodaan kategoriat'''
        obj = self.make_expnsobjs()
        # luodaan kategoria
        expnsobjs = [i for i in obj.get_expenseobjs()]
        obj.make_category('Hieno kategoria', expnsobjs)
        return obj

    def test_category_make(self):
        '''testaa kategorian luomista'''
        obj = self.make_ctgr()
        # tarkistetaan kategorian nimi ja arvot
        self.assertEqual(obj.get_categories()[0].get_name(), 'Hieno kategoria')
        self.assertEqual(float(obj.get_categories()[0].get_value()), 19.66+12.87)
        # tarkistetaan että kategorian sisältämät expenseobjt ei ole toplotissa (jaotellut)
        self.assertNotIn(obj.get_categories()[0].expenses_in()[0], obj.get_to_plot())
        self.assertNotIn(obj.get_categories()[0].expenses_in()[1], obj.get_to_plot())


    def test_add_to_category(self):
        obj = self.make_ctgr()
        # luodaan lisättävä expenseobj
        to_add = Expenseobj('uusikauppa')
        to_add.add_value(22.3)
        to_add.add_date('03.02.2021')
        obj.add_expenseobjs(to_add)
        obj.add_to_plot(to_add)
        obj.add_to_category([to_add], obj.get_categories()[0])
        # tarkistetaan kategorian arvo
        self.assertEqual(float(obj.get_categories()[0].get_value()), 19.66+12.87+22.3)

    def test_break_category(self):
        # luodaan kategoria
        obj = self.make_ctgr()
        # rikotaan kategoria
        obj.break_category('Hieno kategoria')
        self.assertEqual(len(obj.get_categories()), 0)  # ei pitäisi olla enää kategorioita
        self.assertEqual(obj.get_to_plot()[0].get_name(), 'kirjakauppa')
        self.assertEqual(obj.get_to_plot()[1].get_name(), 'ruokakauppa')    # yksittäiset expenseobjt plotissa
        self.assertEqual(obj.seriesDivided.series.slices()[0].label(), 'kirjakauppa')
        self.assertEqual(obj.seriesDivided.series.slices()[1].label(), 'ruokakauppa')

    def test_importance_points_save(self):
        '''Katsotaan lyhyesti että palauttaa asettaa oikean määrän pisteitä'''
        obj = allExpenses()
        obj.add_expense('kirjakauppa', 19.66, '02.02.2021')
        obj.add_expense('kirjakauppa', 19.66, '02.02.2021')
        obj.add_expense('ruokakauppa', 12.87, '01.02.2021')
        obj.add_expense('vuokra', 500, '02.02.2021')
        order = obj.importance_points()
        self.assertEqual(order[obj.get_expenseobjs()[0]], 1+1) # pisteitä käynneistä
        self.assertEqual(order[obj.get_expenseobjs()[1]], 1)
        self.assertEqual(order[obj.get_expenseobjs()[2]], 6+1) # pisteitä suuresta summasta
        # testataan säästötoiminto
        # luodaan uudet expenseobjt
        expns1 = Expenseobj('kirjakauppa')
        expns1.add_value(19.66*2)
        expns1.add_date('02.02.2021')
        expns1.add_date('02.02.2021')
        expns2 = Expenseobj('ruokakauppa')
        expns2.add_value(12.87)
        expns2.add_date('01.02.2021')
        expns3 = Expenseobj('Vuokra')
        expns3.add_value(500)
        expns3.add_date('02.02.2021')
        obj2 = obj.save_money(501, [expns2, expns1, expns3])    # säästö
        # kaksi ekaa menee nollille
        self.assertEqual(float(obj2.get_expenseobjs()[0].get_value()), 0)
        self.assertEqual(float(obj2.get_expenseobjs()[1].get_value()), 0)
        self.assertEqual(float(obj2.get_expenseobjs()[2].get_value()), 51.19)












if __name__ == "__main__":
    unittest.main()