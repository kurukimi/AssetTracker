from PyQt5.QtChart import QPieSeries, QPieSlice



class Series:
    def __init__(self):

        # Luodaan pieseries ja asetetaan sen koko, Luodaaan layout ja lisätään painikkeet yms.
        self.series = QPieSeries()
        self.series.setPieSize(0.48)
        self.series.setHorizontalPosition(0.48)



    def appendSeries(self, name, value):
        # lisää QpieSeriekseen(joka myöhemmin plotataan) joko jaotellut(to_plot) tai ei jaotellut arvot
        slc = QPieSlice(name, float(value))
        self.series.append(slc)


    def editSliceValue(self, indx, value):
        self.series.slices()[indx].setValue(float(value))




    def removeSlice(self,indx):
        self.series.remove(self.series.slices()[indx])



