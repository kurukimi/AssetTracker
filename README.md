**Rahan seuranta**

1. **Esittely** 
  
Ohjelma luo tilitapahtumat tiedostosta graafisen kuvaajan. Käyttäjä voi 
jaotella menoja kategorioihin, ja luoda säästökuvaajan haluamallaan 
säästösummalla
  
2. **Tiedosto- ja kansiorakenne**  
- code kansiosta löytyy kaikki ohjelman .py tiedostot  
- doc kansiossa sijaitsee suunnitelma ja dokumentti  
- unittests kansiossa löytyy yksikkötestikoodi ja siinä käytettävät  
testitiedostot
  
3. **Asennusohje**  
  
Pääohjelma tarvitsee PyQt5 ja pyqtgraph kirjaston toimiakseen  
Kirjastot voi asentaa komentorivillä komennolla "pip install PyQt5"  
ja "pip install pyqtgraph"
  
4. **Käyttöohje**  
  
- Ohjelma käynnistetään avaamalla GUI tiedosto.
- Tiedoston voi lukea valitsemalla tiedostodialogin vasemmasta yläkulmasta
- Käyttöliittymä on vuorovaikutteinen eli kuluja voi valita klikkaamalla
- Vaihda kuvaajan värit satunnaisiksi väreiksi painamalla "vaihda värit"
- Valitse piirakka- tai rengaskuvaaja dropdown valikosta oikealla yläreunassa
- Luo uusi kategoria valitsemalla kulut ja painamalla "Yhdistä kuluja"
- Vaihda jaoteltuun näkymä valitsemalla "jaoteltu kuvaaja"
- Jaotellussa näkymässä erota kategoria valitsemalla kategoria ja "erota kategoria"
- Luo kuvaaja säästökuvaaja painamalla "säästä", syöttämällä säästettävä summa, ja "hyväksy"