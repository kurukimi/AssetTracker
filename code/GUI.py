from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QAction,
 QVBoxLayout, QHBoxLayout, QCheckBox, QFileDialog, QComboBox, QListWidget, QInputDialog, QLabel, QMessageBox,
                             QDialog, QDoubleSpinBox, QListWidgetItem, QLayout)
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.Qt import Qt, QAbstractItemView
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QLegend
from PyQt5 import QtCore
import sys
import random
from dataread import Dataread
import copy



# Luodaan widgetitt
class WidgetWin(QWidget):
    """WidgetWin-luokassa luodaan widgetit ja widgettien ominaisuudet. Asetetaan pääikkunaan MainWin-luokassa"""
    def __init__(self, expenses=None):
        super(WidgetWin, self).__init__()
        self.setWindowModality(QtCore.Qt.ApplicationModal) # jos monta WidgetWiniä auki, saa käyttää vain päälimmäistä
        # säilötään expenses objekti
        self.allExpenses = expenses
        # Luodaan pieseries ja asetetaan sen koko, Luodaaan layout ja lisätään painikkeet yms.
        self.seriesToPlot = QPieSeries()
        self.layoutR = QVBoxLayout()
        self.layoutR1 = QHBoxLayout()
        self.layoutR2 = QHBoxLayout()
        self.comboBox = QComboBox()
        self.comboBox.addItems(['Piirakkadiagrammi', 'Rengasdiagrammi'])
        self.BtnColor = QPushButton('vaihda värit')
        self.ChkBox = QCheckBox('Jaoteltu kuvaaja')
        self.BtnMerge = QPushButton('yhdistä kuluja')
        self.BtnBreak = QPushButton('erota kategoria')
        self.BtnSave = QPushButton('säästä')
        # Luodaan chartview widgetti ja lisätään siihen luotu kuvaaja chart
        self.chartView = QChartView()
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chart = QChart()
        self.series2 = self.allExpenses.seriesDivided.series    # jaoteltu ja
        self.series = self.allExpenses.Series.series   # ei jaoteltu series
        self.currentSeries = self.series # nykyinen series joka näkyvissä
        self.chart.addSeries(self.series)
        self.chart.addSeries(self.series2)
        self.series2.setVisible(False)
        self.chartView.setChart(self.chart)
        # lisätään painikkeet, checkboksit yms. layoutteihin
        self.layoutR1.addWidget(self.comboBox)
        self.layoutR1.addWidget(self.BtnColor)
        self.layoutR2.addWidget(self.BtnMerge)
        self.layoutR2.addWidget(self.BtnBreak)
        self.layoutR.addLayout(self.layoutR1)
        self.layoutR2.addWidget(self.ChkBox)
        self.layoutR.addLayout(self.layoutR2)
        self.layoutR.addWidget(self.BtnSave)
        # Muodostetaan 'kokonaislayout' johon asetetaan aiemmat layoutit
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.chartView, 90)
        self.layout.addLayout(self.layoutR, 5)
        self.setLayout(self.layout)
        # muuttuja ja funktiot värien vaihtamiseksi
        self.color = None
        self.colors()
        # asetetaan buttoneita pois käytöstä, kunnes tietty ehto kohdataan
        self.BtnMerge.setEnabled(False)
        self.BtnBreak.setEnabled(False)
        self.BtnBreak.setVisible(False)
        self.ChkBox.setEnabled(False)
        self.BtnSave.setEnabled(False)
        # Liitetään buttonit ja checkboksit yms. toimintoihin(funktioihin)
        self.ChkBox.stateChanged.connect(self.chkboxAction)
        self.comboBox.activated[str].connect(self.cisActivated)
        self.BtnColor.clicked.connect(self.colors)
        self.BtnColor.clicked.connect(self.setChartColors)
        self.series.clicked.connect(self.sliceClick)
        self.series2.clicked.connect(self.sliceClick)
        self.series.hovered.connect(self.sliceHover)
        self.series.doubleClicked.connect(self.sliceDoubleClick)
        self.series2.hovered.connect(self.sliceHover)
        self.series2.doubleClicked.connect(self.sliceDoubleClick)
        self.BtnMerge.clicked.connect(self.showDialog)
        self.BtnBreak.clicked.connect(self.btnBreakAction)
        self.BtnSave.clicked.connect(self.saveDialog)
        # säästökuvaaja ja säästetty määrä
        self.save = None
        self.saved = ''
        self.setChart()


    def legendMarkerClick(self, lgnd):
        # kun klikataan kaavion palasen otsikkoa, halutaan, että tapahtuu sama kun klikattaisiin kaavion palasta
        self.sliceClick(lgnd.slice())

    def legendMarkerHover(self, bol, lgnd):
        # kun hiiri on kaavion palasen otsikon päällä, tehdään sama kun se olisi kaavion palasen päällä
        self.sliceHover(lgnd.slice(), bol)

    def connectLegend(self):
        # luodaan legendmarkereille eli kaavion palasten otsikoille click yhteys
        for marker in self.chart.legend().markers(self.currentSeries):
            marker.disconnect()
            marker.clicked.connect(lambda lgnd=marker: self.legendMarkerClick(lgnd))
        for marker in self.chart.legend().markers(self.currentSeries):
            marker.hovered.connect(lambda bol, lgnde=marker: self.legendMarkerHover(bol, lgnde))

    def chkboxAction(self):
        # asetetaan slicet neutraaleiksi
        # jos checkbox on painettu: asetetaan erota nappi näkyviin ja yhdistä nappi pois näkyvistä
        # ja jaoteltu kuvaaja asetetaan näkyviin
        # checkbox ei painettu: yhdistänappi näkyviin, erota nappi pois näkyvistä, jaottelematon kuvaaja näkyviin
        self.setSliceNeutral()
        if self.ChkBox.isChecked():
            self.BtnMerge.setEnabled(False)
            if 'säästö' not in self.chart.title():
                self.BtnMerge.setVisible(False)
                self.BtnBreak.setVisible(True)
            self.series.setVisible(False)
            self.series2.setVisible(True)
            self.currentSeries = self.series2
            self.createChart()

        else:
            self.BtnBreak.setEnabled(False)
            if 'säästö' not in self.chart.title():
                self.BtnBreak.setVisible(False)
                self.BtnMerge.setVisible(True)
            self.series2.setVisible(False)
            self.series.setVisible(True)
            self.currentSeries = self.series
            self.createChart()


    def cisActivated(self, text):
        # Valitsee diagrammin comboboxin arvon mukaan: piirakka tai donitsidiagrammi
        if text == 'Piirakkadiagrammi':
            self.series.setHoleSize(0)
            self.series2.setHoleSize(0)
        elif text == 'Rengasdiagrammi':
            self.series.setHoleSize(0.4)
            self.series2.setHoleSize(0.4)


    def createChart(self):
        #  päivitetään aktiivisen kuvaajan markerlabelit ja otsikko
        # asetetaan säästönappi painettavaksi
        # yhdistetään markerit aktiiviseen kuvaajaan
        self.chartSlices()
        self.setChart()
        self.BtnSave.setEnabled(True)
        self.connectLegend()

    def chartSlices(self):
        # Astetetaan otsikot piirakan osille. Jos osa on jossain kategoriassa, lisätään kategorian nimi teksti otsikkoon
        ctgr = ''
        for slice, marker, expnsobj in zip(self.currentSeries.slices(), self.chart.legend().markers(self.currentSeries), self.allExpenses.get_expenseobjs()):
            if expnsobj.get_category() and expnsobj.get_name() == slice.label():
                ctgr = '<sup style="color:Red;">({})</sup>'.format(expnsobj.get_category().get_name())
            if slice.label() not in [obj.get_name() for obj in self.allExpenses.get_expenseobjs()]:
                marker.setLabel(
                    '{:.2f}e ({:.2f}%);<b>{}</b>'.format(slice.value(), slice.percentage() * 100, slice.label()))
            else:
                marker.setLabel('{:.2f}e ({:.2f}%);{}{}'.format(slice.value(), slice.percentage()*100, ctgr, slice.label()))
            ctgr = ''


    def setChart(self):
        # Asetetaan kuvaaja: lisätään QpieSeries kuvaajaan, lisätään kuvaajan otsikko, lisätään otsikon määritykset
        # Lisätään kuvaajan animaatiot
        if len(self.chart.series()) < 1:
            self.chart.addSeries(self.series)
        if self.series.isEmpty():
            self.chart.setTitle('Lisää tiedosto')
        else:
            self.chart.setTitle('yhteensä: {:.2f}e {}'.format((self.series.sum()), self.saved))
        self.chart.setTitleFont(QFont('Times', 15, QFont.Bold))
        self.chart.legend().setAlignment(Qt.AlignLeft)
        self.chart.legend().setMarkerShape(QLegend.MarkerShapeRectangle)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setAnimationDuration(500)

    def colors(self):
        # valitaan satunnaiset värit ja säilötään ne instanssimuuttujaan, jolloin voidaan hallitusti muuttaa sitä
        color = []
        for i in range(len(self.allExpenses.get_expenseobjs())):
            color.append(QColor(random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)))
        self.color = color

    def setChartColors(self):
        # Asetetaan satunnaiset värit kaaviolle
        for slice, color in zip(self.currentSeries.slices(), self.color):
            slice.setBrush(color)

    def sliceClick(self, slice):
        # Voidaan valita kaavion osat klikkaamalla ja näytetään 'exploded' efekti, osan label.
        sumExp = 0
        if slice.isExploded():
            slice.setExploded(False)
            slice.setLabelVisible(False)
            self.chart.setTitle('yhteensä: {:.2f}e {}'.format((self.series.sum()), self.saved))
        else:
        # jos slice ei ole 'exploded' eli valittu, niin klikkauksesta asetetaan se:
            slice.setExploded()
            slice.setLabelVisible()
            slice.setLabelArmLengthFactor(0.1)
        # Lasketaan valittujen kulujen summa ja näytetään otsikossa
        for i in self.currentSeries.slices():
            if i.isExploded():
                sumExp += i.value()
                self.chart.setTitle('yhteensä: {:.2f}e {} ({:.2f} -> {}%)'.format(self.series.sum(), self.saved
                                                                                  , sumExp, int((sumExp/self.series.sum()
                                                                                                )*100)))
        # Hieman pitkähköt listcomprehensionit:
        # Jos sliceja valittuna(exploded), ja ne ei ole kategorioita, niin asetetaan yhdistä-nappi painettavaksi
        # Jos yksikään valittu slice on jossain kategoriassa, niin yhdistä-nappi ei ole painettavissa
        # jos sliceja ei valittu, yhdista-nappi ei painettavissa
        if [j.isExploded() for j in self.series.slices() if
            j.label() not in [a.get_name() for b in [i.expenses_in() for i in self.allExpenses.get_categories()]
            for a in b]].count(True) > 0 and [j.isExploded() for j in self.series.slices() if
            j.label() in [a.get_name() for b in
                          [i.expenses_in() for i in self.allExpenses.get_categories()] for a in b]].count(True) < 1 \
                and not self.ChkBox.isChecked():
            self.BtnMerge.setEnabled(True)
        else:
            self.BtnMerge.setEnabled(False)
        # Jos jaottelu on päällä, ja valittuna(exploded) on kategorioita ja valittuna ei ole muuta (expenseobj)
        # , niin asetetaan erota-nappi painettavaksi
        if self.ChkBox.isChecked() and [j.isExploded() for j in self.series2.slices() if
            j.label() in [i.get_name() for i in self.allExpenses.get_categories()]].count(True) > 0 \
                and [j.isExploded() for j in self.series2.slices() if
            j.label() not in [i.get_name() for i in self.allExpenses.get_categories()]].count(True) < 1:
            self.BtnBreak.setEnabled(True)
        else:
            self.BtnBreak.setEnabled(False)

    def sliceDoubleClick(self):
        # Suurennetaan/pienennetään kaaviota tuplaklikkauksella
        if self.currentSeries.pieSize() != 1:
            self.currentSeries.setPieSize(1)
        else:
            self.currentSeries.setPieSize(0.48)

    def sliceHover(self, slice, bool):
        # Tummennetaan kaavion osan ("slice") reunat kun hiiri on kohdalla
        if not slice.borderColor() == QColor(255, 0, 0):
            if bool:
                slice.setBorderColor(QColor(0, 0, 0))
                slice.setBorderWidth(3)
            elif not bool and not slice.isExploded():
                slice.setBorderWidth(0)
                slice.setBorderColor(QColor(255, 255, 255))

    def showDialog(self):
        # popup dialogi jaottelun nimen asettamiseksi
        dial = QInputDialog(self)
        dial.setWindowTitle('Luo/lisää kategoriaan')
        dial.setLabelText('Anna kategorian nimi:')
        dial.resize(500, 300)
        ok = dial.exec_()
        text = dial.textValue()
        # Jos saadaan tekstiä ja painetaan 'ok', ja on pelkkiä kirjaimia niin lisätään valitut osat listaan lis
        if ok and 25 > len(str(text)) > 0 and text.isalpha():
            text = text.upper()
            lis = [i for i in self.allExpenses.get_expenseobjs()
                   if i.get_name() in [j.label() for j in self.series.slices() if j.isExploded()]]
        # Asetetaan slicet takaisin neutraaleiksi
            for slice in self.series.slices():
                if slice.isExploded():
                    self.setSliceNeutral()
        # Luodaan kategoriat expenses olioon, asetetaan buttonit
        # mahdolllisuus lisätä kuluja jo olemassa olevaan kategoriaan syöttämällä jo olemassa olevan ktgrian nimi
            is_ctgr = False
            for i in self.allExpenses.get_categories():
                if str(text) == i.get_name():
                    is_ctgr = True
                    self.allExpenses.add_to_category(lis, i)
            if not is_ctgr:
                self.allExpenses.make_category(str(text), lis)
            self.createChart()
            self.BtnMerge.setEnabled(False)
            self.ChkBox.setEnabled(True)
        # virheviestit virheelliselle syötteelle
        elif ok:
            msg = QMessageBox()
            msg.setWindowTitle('Virhe')
            if len(text) < 1 or len(text) >= 25:
                message = 'Nimen pituus tulee olla 1-24'
            else:
                message = 'Käytä ainoastaan kirjaimia'
            msg.setText('Virheellinen syöte<br>{}'.format(message))
            msg.exec_()


    def btnBreakAction(self):
        # Funktio suoritetaan kun erota-nappia painetaan
        # jos osia valittuna, niin rikotaan/poistetaan niitten kategoria, ja
        # päivitetään taas kuvaaja uudella datalla(createchart)
        if [i.isExploded() for i in self.series2.slices()].count(True) > 0:
            for i in self.series2.slices():
                if i.isExploded():
                    self.allExpenses.break_category(i.label())
            self.createChart()
            self.BtnBreak.setEnabled(False)
        # Jos kategoriat loppuu jaottelu-näkymästä, niin näytetään ei-jaoteltu näkymä
        if len(self.allExpenses.get_categories()) < 1:
            self.ChkBox.setChecked(False)
            self.ChkBox.setEnabled(False)

    def setSliceNeutral(self):
        # asettaa pois kaikki sliceen lisätyt efektit
        for slc in self.currentSeries.slices():
            slc.setExploded(False)
            slc.setLabelVisible(False)
            slc.setBorderWidth(0)
            slc.setBorderColor(QColor(255, 255, 255))
            self.chart.setTitle('yhteensä: {:.2f}e {}'.format((self.series.sum()), self.saved))

    def saveDialog(self):
        '''funktio luo uuden WidgetWin olion, jossa näytetään säästökuvaaja'''
        self.createChart()
        def savef():
            lis = []
            # kopioidaan nykyisen expenses olion menot
            for i in [str(listWid.itemWidget(listWid.item(j)).layout().itemAt(0).widget().text()) for j in range(listWid.count())]:
                for k in self.allExpenses.get_expenseobjs():
                    if '</sup>' in i:
                        h = i.split('</sup>')[1]
                    else:
                        h = i
                    if h == k.get_name():
                        lis.append(k)
            expns = self.allExpenses.save_money(spinBox.value(), copy.deepcopy(lis))  # Series oliot
            self.save = WidgetWin(expns) # uusi WidgetWin olio, ja tallennetaan se 'pääwidgetin' self.saveen
            # asetetaan säästökuvaajaan tarpeettomat nappulat pois, ja lisätään muut arvot otsikot yms.
            if len(self.allExpenses.get_categories()) > 0:
                self.save.ChkBox.setEnabled(True)
            self.save.BtnBreak.hide()
            self.save.BtnMerge.hide()
            self.save.BtnSave.hide()
            self.save.saved = '<sup style="color:Red;">säästö: {}e</sup>'.format(spinBox.value())
            self.save.createChart()
            self.save.resize(1400, 600)
            self.save.setWindowTitle('säästökuvaaja')
            self.save.show()
        QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        # luodaan liswidgetti, jossa näytetään 'AI':lla luotu säästöjärjestys
        # ja annetaaan käyttäjän muokata järjestystä
        # lisätään myös napit, tekstit yms.
        saveDial = QDialog()
        saveDial.resize(600, 600)
        saveDial.setWindowTitle('Ehdotettu säästöjärjestys')
        layout = QVBoxLayout()
        listWid = QListWidget()
        button = QPushButton('Hyväksy')
        buttonc = QPushButton('Peruuta')
        buttonc.clicked.connect(saveDial.close)
        button.clicked.connect(savef)
        button.clicked.connect(saveDial.close)
        spinBox = QDoubleSpinBox()
        spinBox.setMinimum(1)
        spinBox.setMaximum(self.series.sum()-0.01)
        labl = QLabel('Kuluista säästetään järjestyksessä ylhäältä alaspäin<br>'
                      'raahaa objekteja muokataksesi järjestystä')
        labl2 = QLabel('Säästettävä summa:')
        listWid.setDragDropMode(QAbstractItemView.InternalMove)
        # lasketaan tärkeysjärjestys
        dic = self.allExpenses.importance_points()
        for i in dic:
            cat = ''
            widgItem = QListWidgetItem()
            widget = QWidget()
            if i.get_category():
                cat = '<sup style="color:Red;">({})</sup>'.format(i.get_category().get_name())
            text = QLabel('{}{}'.format(cat, i.get_name()))
            widgetLayout = QHBoxLayout()
            widgetLayout.addWidget(text)
            widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
            widget.setLayout(widgetLayout)
            listWid.addItem(widgItem)
            widgItem.setSizeHint(widget.sizeHint())
            listWid.setItemWidget(widgItem, widget)
        # lisätään dialog ikkunaan luodut nappulat, widgetit yms.
        layout.addWidget(labl)
        layout.addWidget(listWid)
        layout.addWidget(labl2)
        layout.addWidget(spinBox)
        btns = QHBoxLayout()
        btns.addWidget(button)
        btns.addWidget(buttonc)
        layout.addLayout(btns)
        saveDial.setLayout(layout)
        saveDial.exec()

# Luodaan ohjelman pääikkuna
class MainWin(QMainWindow):
    """MainWin-luokka on ohjelman pääikkuna. Pääikkunassa aloitamme ohjelman toimintaa valitsemalla luettava
    tiedosto, ja luomalla tämän mukaan widgetti"""
    def __init__(self):
        super().__init__()
        # aloitetaan Dataread, siitä saadulla datalla Expenses, ja siitä widget
        self.dataread = Dataread()
        self.expenses = self.dataread.get_expenses()
        self.widget = WidgetWin(self.expenses)
        # Luodaan pääikkunan asetukset ja ominaisuudet
        self.resize(1600, 800)
        self.setWindowTitle('Rahan seuranta')
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('Tiedosto')
        # Asetetaan WidgetWin luokan widgetti 'central' widgetiksi
        self.setCentralWidget(self.widget)
        # Lisätään tiedostodialogi toiminto tiedostomenuun
        fileOpen = QAction('Open File', self)
        fileOpen.triggered.connect(self.file_open)
        self.fileMenu.addAction(fileOpen)

    def errwin(self):
        # Näytetään virheviesti, jos tiedostonlukemisessa tapahtuu virhe
        msg = QMessageBox()
        msg.setWindowTitle('Virhe')
        msg.setText('Virheellinen tiedosto')
        msg.exec_()

    def file_open(self):
        # Tiedostodialogin ajo: sisällytetään vain csv
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', filter='csv(*.csv)')
        # jos tiedostonluku ei tapahdu oletetusti: tiedostossa jotain vikaa, näytetään virheviesti
        if name:
            try:
                self.dataread.add_file(name)
                self.expenses = self.dataread.get_expenses()  #luetaan tiedot expenses luokkaan
                self.widget.createChart() # luodaan kuvaaja
                # set_to_plot:iin
                self.setCentralWidget(self.widget)
            except (IndexError, ValueError):
                self.errwin()
                # jos tiedostossa oli kuitenkin joitain oikeita rivejä, niin luodaan chartti niistä
                if len(self.widget.series) > 0:
                    self.widget.createChart()






# GUI:n ajo
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.exit(app.exec_())


