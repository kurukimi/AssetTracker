from expensecategory import Expensecategory
from expense import Expense
from expenseobj import Expenseobj
from series import Series
import statistics
from decimal import Decimal
import datetime


class allExpenses:
    """Expenses -luokan tarkoitus on säilyttää ostotapahtuma(expense), kulut(expenseobj) ja
    kulukategoria(expenseCategory) -luokat käytettävissä listoissa ja käsitellä niitä
    mm. luomalla ostotapahtumista(expense) kuluja(expenseobj), luomalla kuluista(expenseobj)
    kulukategorioita(expensecategory) ja luomalla lista plotattavista kuluista (jaottelu vai ei jaottelu)"""
    def __init__(self):
        self.expenses = []
        self.expenseobjs = []
        self.expenseCategories = []
        self.dividedExpenses = []
        self.Series = Series()
        self.seriesDivided = Series()
        self.names = []

    def get_expenses(self):
        return self.expenses  # ostotapahtumat (expense)

    def set_expenses(self, expns):
        self.expenses = expns   # asettaa ostotapahtumat (expense)

    def set_expenseobjs(self, expns):
        self.expenseobjs = expns[:] # asettaa kulut (expenseobj)


    def add_expense(self, name, value, date):
        expns = Expense(name, value, date)  # luo expense olion
        self.expenses.append(expns) # lisää sen listaaan
        self.create_objects(expns) # luo yksittäisistä ostotapahtumista (expense) kuluja (expenseobj)



    def create_objects(self, expense):
        # Muodostetaan Expenseobj oliot, lisätään ne listoihin, ja serieksiin
        lis = []
        name = expense.get_name()
        value = expense.get_value()
        if len(self.expenseobjs) > 0:
            lis = [i.get_name() for i in self.expenseobjs]
        if expense.get_name() not in lis:
            # jos ei vielä lisätty, niin lisätään uusi olio
            obj = Expenseobj(name)
            obj.add_value(value)
            obj.add_date(expense.get_date())
            self.add_to_plot(obj)
            self.add_expenseobjs(obj)
        else:
            # jos listassa on jo kauppa nimellä, ei lisätä uutta, vaan muokataan vain arvoja
            indx = lis.index(expense.get_name())
            self.expenseobjs[indx].add_value(expense.get_value())
            self.expenseobjs[indx].add_date(expense.get_date())
            self.Series.editSliceValue(indx, self.expenseobjs[indx].get_value())
            # Seriekseen pitää lisätä kategorian arvo erikseen koska vaikka kategoria päivittyy kun lisätään arvo
            # Expenseobj:hin, niin ne ei ole mitenkään linkitetty seriekseen.
            if self.expenseobjs[indx].get_category():
                # jos kauppa, johon ollaan lisäämässä arvoa on jossain kategoriassa, muokataan muokataan
                # jaoteltuun seriekseen (seriesToPlot)
                # kategorian uusi arvo
                self.update_category()
                indx2 = self.dividedExpenses.index(self.expenseobjs[indx].get_category())
                self.seriesDivided.editSliceValue(indx2, self.expenseobjs[indx].get_category().get_value())
            else:
                # jos ei kategoriassa, niin lisätään kulun uusi arvo
                indxx = self.dividedExpenses.index(self.expenseobjs[indx])
                self.seriesDivided.editSliceValue(indxx, self.expenseobjs[indx].get_value())


    def add_expenseobjs(self, obj):
        # lisätään expenseobj listaan ja seriekseen
        self.expenseobjs.append(obj)
        self.Series.appendSeries(obj.get_name(), obj.get_value())

    def set_to_plot(self, expns):
        # asetetaan toPlotExpenseihin eli jaoteltuihin expenseihin
        self.dividedExpenses = []
        self.dividedExpenses = expns[:]

    def add_to_plot(self, expns):
        # lisätään jaoteltuihin kuluihin ja seriekseen
        self.dividedExpenses.append(expns)
        self.seriesDivided.appendSeries(expns.get_name(), expns.get_value())



    def remove_from_plot(self, expns):
        # poistaa kulun jaotelluista kuluista ja serieksestä
        indx = self.dividedExpenses.index(expns)
        self.seriesDivided.removeSlice(indx)
        self.dividedExpenses.remove(expns)


    def get_to_plot(self):
        return self.dividedExpenses

    def get_expenseobjs(self):
        return self.expenseobjs

    def update_category(self):
        # Päivittää kategoriat: jos lisätätään dataa, ja datassa on samoja kohteita mitä on jo jaoteltu(category), niin
        # päivittää kategorioiden arvot.
        for expns in self.expenseobjs:
            if expns.get_category():
                expns.get_category().value_calc()



    def make_category(self, name, expenseobjs):
        # luo uuden kategorian
        category = Expensecategory(name, expenseobjs)
        self.expenseCategories.append(category)
        # päivittää samalla jaotellut menot poistamalla Expenseobj ja lisäämällä kategorian
        for expenseobj in expenseobjs:
            self.remove_from_plot(expenseobj)
            expenseobj.in_category(category, True)
        self.add_to_plot(category)


    def add_to_category(self, expenseobjs, category):
        # jos kategoria jo olemassa ei luoda uutta vaan lisätään olemassaolevaan kategoriaan
        category.add_expenses(expenseobjs)
        indx = self.dividedExpenses.index(category)
        self.seriesDivided.editSliceValue(indx, category.get_value())
        for expenseobj in expenseobjs:
            self.remove_from_plot(expenseobj)
            expenseobj.in_category(category, True)

    def break_category(self, name):
        # poistaa kategorian
        for category in self.expenseCategories:
            if name == category.get_name():
                for expenseobj in category.expenses_in():
                    self.add_to_plot(expenseobj)
                    expenseobj.in_category(category, False)
        # päivittää jaotellut menot poistamalla kategorian ja lisäämällä takaisin sen sisältämät Expenseobj
                self.remove_from_plot(category)
                self.expenseCategories.remove(category)


    def get_categories(self):
        return self.expenseCategories


    def importance_points(self):
        for obj in self.get_expenseobjs():
            obj.clear_importance()
        # Funktio laskee tärkeyspisteet expenseobj:lle alla kerrottujen menettelyjen mukaan
        alldates = []
        alldiff = []
        stores = self.get_expenseobjs()
        # lasketaan ensin kaikkien kauppojen yhteinen
        dates = []
        datesDiff = []
        datelist = [i.get_date() for i in stores]
        get_date = [st for x in datelist for st in x]
        for date in get_date:
            year = int(date.split('.')[2])
            month = int(date.split('.')[1])
            day = int(date.split('.')[0])
            dates.append(datetime.datetime(year, month, day)) # datetime objektit
        dates.sort()    # aikajärjestykseen
        # lasketaan aikaerot ostosten välillä
        for i in range(1, len(dates)):
            diff = dates[i]-dates[i-1]
            diff = diff.days
            datesDiff.append(diff)
        alldiff.extend(datesDiff)
        alldates.extend(dates)
        devall = statistics.pstdev(alldiff)  # keskihajonta kaikkien kauppakäyntien aikaväleistä
        devalueall = statistics.pstdev([i.get_value() for i in self.expenses])   # keskihajonta kaikkien maksujen suuruudesta
        meanall = statistics.mean([i.get_value() for i in self.expenses]) # keskiarvo kaikista maksuista
        # sitten lasketaan jokaisen kaupan oma ja verrataan keskivertoihin
        for expenseobj in stores:
            dates = []
            datesDiff = []
            get_date = expenseobj.get_date()
            for date in get_date:
                expenseobj.increase_importance(1)  # tärkeyspisteitä käyntikerroista +1
                # luodaan datetime objekti ja lisätään listaan
                year = int(date.split('.')[2])
                month = int(date.split('.')[1])
                day = int(date.split('.')[0])
                dates.append(datetime.datetime(year, month, day))
            dates.sort()
            # jos käyntejä enemmän kuin 2: lasketaan käyntien välien
            # keskihajonta: ideana kasvattaa tärkeyttä jos kuluttaminen tiettyyn kohteeseen on säännöllistä
            # jos keskihajonta kaupassa on pienempi kuin kaikkien kauppojen keskihajonta, niin kasvatetaan pisteitä
            for i in range(1, len(dates)):
                diff = dates[i]-dates[i-1]
                diff = diff.days
                datesDiff.append(diff)
            if len(datesDiff) > 1:
                dev = statistics.stdev(datesDiff)
                if dev < devall:
                    expenseobj.increase_importance(2)
            # Lasketaan maksun suuruuden keskiarvo tiettyyn kauppaan (kokosumma kauppaan/käynnit kaupassa)
            # jos suurempi kuin keskihajonta kaikkien maksujen suuruudesta + keskiarvo kaikista maksuista
            # , niin kasvatetaan tärkeyttä
            # idea: yleensä hinnakkaat yksittäismaksut viittaavat tärkeään kuluun esim. vuokra
            if expenseobj.get_value()/len(dates) > devalueall+meanall:
                expenseobj.increase_importance(6)
        # lisätään kaupat arvoineen sanakirjaan ja järjestetään arvon mukaan pienimmästä suurimpaan
        dic = {}
        for expenseobj in stores:
            dic[expenseobj] = expenseobj.get_importance()
        dic = dict(sorted(dic.items(), key=lambda item: item[1]))
        return dic


    def save_money(self, amount, ordr):
        # funktio luo uuden Expenses olion, johon lisätään uudet säästetyt seriekset
        # ja luodaan ja säilötään säästetyt menot ja kategoriat
        order = ordr   # käyttäjän hyväksymä järjestys menoista säästämiselle
        amount = Decimal(amount)
        # uudet series oliot joista säästetään
        saveSeries = Series()
        saveSeriesToPlot = Series()
        # vähennetään uusien Expenseobj:en menoista haluttu summa annetussa järjestyksessä
        # vähennetään ensin ensimmäisestä, ja mennään seuraavaan jos ensimmäinen menee nollaan
        for obj in order:
            if amount > 0:
                if amount >= obj.get_value():
                    amount -= obj.get_value()
                    obj.value = Decimal(0)
                elif amount < obj.get_value():
                    obj.value = obj.value - amount
                    amount = 0
        # päivitetään kategoriat
        for i in order:
            if i.get_category():
                i.get_category().value_calc()
        # lisätään säästetyistä expenseobj:sta arvot jaottelemattomaan saveSeriekseen ja jaoteltuun saveSeriesToPloT:iin
        for obj in order:
            saveSeries.appendSeries(obj.get_name(), obj.get_value())
            if obj.get_category():
                if obj.get_category().get_name() not in [slc.label() for slc in saveSeriesToPlot.series.slices()]:
                    saveSeriesToPlot.appendSeries(obj.get_category().get_name(), obj.get_category().get_value())
            else:
                saveSeriesToPlot.appendSeries(obj.get_name(), obj.get_value())
        expns = allExpenses() # uusi Expenses olio
        # asetetaan muokatut Expenseobjt, kategoriat ja seriekset
        expns.set_expenseobjs(ordr[:])
        expns.expenseCategories = [i.get_category() for i in order if i.get_category()]
        expns.seriesDivided = saveSeriesToPlot
        expns.Series = saveSeries
        return expns
