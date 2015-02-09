import csv
import math
from itertools import permutations

# joulupukki.py on harjoitustyö, jonka avulla opettelin Python 3:a.
# Tehtävänä on laskea lyhin reitti joulupukille 10 maailman suurimman kaupungin läpi, lähtien
# Korvatunturilta. Ongelma perustuu Tieteellinen laskenta II  (Helsingin yliopisto) kurssin
# lopputyötehtävään ja ns. kauppamatkustajan ongelmaan.
#
# HUOM! ohjelma ei lataa kaupunkidataa automaattisesti, vaan tiedosto tulee ladata itse:
# https://www.maxmind.com/en/free-world-cities-database
#
# Juhani Takkunen
# juhani.takkunen@helsinki.fi
# tel. 0407025967

##### Määritellään luokat #####

class Kaupunki:
    # luokka määrittää kaupunkien perusominaisuudet: nimi, asukasmäärä sekä koordinaatit

    def __init__(self, object):
        # konstruktori-parametri on samaa muotoa, kuin worldcitiespop.txt - csv-tiedosto, eli:
        # Country,City,AccentCity,Region,Population,Latitude,Longitude
		# lähde: (https://www.maxmind.com/en/free-world-cities-database)
        # - tiedot voidaan antaa string-muodossa
        self.nimi = object[2]
        try:
            self.asukasmaara = int(object[4])
        except ValueError:
            self.asukasmaara = 0
        self.lat = float(object[5])
        self.lon = float(object[6])
        self.etaisyydet = {}

    @classmethod
    def Korvatunturi(cls):
        # Koska Korvatunturia ei löydy csv-tiedostosta, luodaan tiedot käsin
        nimi = "Korvatunturi"
        asukasmaara = "10" # Joulupukki, Joulumuori ja pari tonttua
        lat = "70.0833" # http://zip-code.en.mapawi.com/finland/16/k/1/10/korvatunturi/77777/3516/
        lon = "27.85"
        return cls(["", "", nimi, "", asukasmaara, lat, lon])


    def etaisyysKaupunkiin(self, toinenKaupunki):
        # Lasketaan etäisyys tämän ja jonkin toisen Kaupungin välillä. Tallennetaan laskettu
        # etäisyys (etaisyydet),jotta niitä ei tarvitse myöhemmin laskea uudelleen.
        # -> Palautetaan etäisyys kilometreinä
        if toinenKaupunki.nimi not in self.etaisyydet:
            self.etaisyydet[toinenKaupunki.nimi] = laskeEtaisyys(self, toinenKaupunki)
        return self.etaisyydet[toinenKaupunki.nimi]

#### MÄÄRITELLÄÄN FUNKTIOT ####

def laskeEtaisyys(kaupunki1, kaupunki2):
    # laskee etäisyyden kahden kaupungin(olio) välille.
    # Alkuperäinen ohje: http://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
	# -> Palauttaa kahden kaupungin välisen etäisyyden [km]
    R = 6371 # maapallon säde [km]
    dLat = math.radians(kaupunki1.lat - kaupunki2.lat)
    dLon = math.radians(kaupunki1.lon - kaupunki2.lon)

    lat1 = math.radians(kaupunki1.lat)
    lat2 = math.radians(kaupunki2.lat)

    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    etaisyys = R * c

    return etaisyys

def laskeMatka(reitti):
	# Laskeen annettujen kaupunkien läpi kuljetun reitin annetussa järjestyksessä.
	# - reitin tulee olla taulukko/tuple, jonka alkioina on Kaupunkeja.
	# - palautetaan kokonaismatka [km]
    kokonaismatka = 0
    for i in range(len(reitti)-1):
        kokonaismatka += laskeEtaisyys(reitti[i], reitti[i+1])
    return kokonaismatka

#### PÄÄOHJELMA ALKAA ####

# Etsitään maapallon suurimpien kaupungin nimet ja koordinaatit ja järjestetään
# suuruusjärjestykseen suurimmasta alkaen. Lähdetiedosto kopioitu sivulta:
# https://www.maxmind.com/en/free-world-cities-database 3.2.2015
with open('worldcitiespop.txt', 'rt', encoding="latin1") as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    next(data, None)  # skip the headers
    kaupungit = [Kaupunki(rivi) for rivi in data]
    kaupungit.sort(key=lambda x: x.asukasmaara, reverse=True)

# Määritetään, minkä kaupunkien läpi joulupukki kulkee - tässä tilanteessa valitsemme
# nyt, että suurimpien kaupunkien. Koska tekniikka vaatii paljon laskentatehoa,
# en suosittele yli 10 kaupungin laskemista.
nKaupungit = 10
suurimmatKaupungit = kaupungit[0:nKaupungit]
print("suurimmat kaupungit ovat:")
for x in suurimmatKaupungit:
    print(x.nimi, x.asukasmaara)

# Koska joulupukki asuu Korvatunturilla, lisätään se lähtöpisteeksi.
# Muiden kaupunkien läpi käydään reitti kaikkien reittipermutaatioiden läpi ja etsitään,
# mikä on lyhin reitti. Permutaatiot kuvaavat kaikkia erilaisia reittejä siten, että samassa
# kaupungissa ei pysähdytä kahdesti.
print("*************************")
print("== ALOITETAAN LASKENTA ==")
print("*************************")

korvatunturi = Kaupunki.Korvatunturi()
for reitti in permutations(suurimmatKaupungit):
    matka = laskeMatka((korvatunturi,) + reitti)
    pieninMatka = float("Inf")
    if matka < pieninMatka:
        pieninMatka = matka
        pieninReitti = (korvatunturi,) + reitti


# Tulostetaan saadut tulokset näytölle
print("==========================")
print("Pienin matka on:")
print(pieninMatka)
print("========================== \n")
print("Reitti")
print("Kaupunki, asukasluku, latitude, longitude")
for i in pieninReitti:
    print(i.nimi, i.asukasmaara, i.lat, i.lon)