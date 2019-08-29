import argparse
import csv
import math
from itertools import permutations
# joulupukki.py on harjoitustyö, jonka avulla opettelin Python 3:a.
# Tehtävänä on laskea lyhin reitti joulupukille 10 maailman suurimman
# kaupungin läpi, lähtien Korvatunturilta. Ongelma perustuu Tieteellinen
# laskenta II (Helsingin yliopisto) kurssin lopputyötehtävään ja ns.
# kauppamatkustajan ongelmaan.
#
# 2019-08-29: Päivitin koodia hieman, jotta pystyin käyttämään tätä vanhaa
#             koodia Docker-testaukseen.
from typing import Iterable

from tabulate import tabulate


class City:

    def __init__(self, name, pop, lat, lon):
        self.name: str = name
        self.pop: int = pop
        self.lat: float = lat
        self.lon: float = lon
        self._distances_to_other_cities = {}

    @classmethod
    def Korvatunturi(cls):
        # Koska Korvatunturia ei löydy csv-tiedostosta, luodaan tiedot käsin
        nimi = "Korvatunturi"
        asukasmaara = 10  # Joulupukki, Joulumuori ja pari tonttua

        # http://zip-code.en.mapawi.com/finland/16/k/1/10/korvatunturi/77777/3516/
        lat = 70.0833
        lon = 27.85
        return cls(nimi, asukasmaara, lat, lon)

    def distance_to_city(self, other_city):
        # Lasketaan etäisyys tämän ja jonkin toisen Kaupungin välillä. 
        # Tallennetaan laskettu etäisyys (etaisyydet),jotta niitä ei 
        # tarvitse myöhemmin laskea uudelleen.
        # -> Palautetaan etäisyys kilometreinä
        if other_city.nimi not in self._distances_to_other_cities:
            self._distances_to_other_cities[other_city.nimi] = calc_distance(self, other_city)
        return self._distances_to_other_cities[other_city.nimi]


def calc_distance(kaupunki1, kaupunki2):
    # laskee etäisyyden kahden kaupungin(olio) välille.
    # Alkuperäinen ohje: 
    # http://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
    # -> Palauttaa kahden kaupungin välisen etäisyyden [km]
    R = 6371  # maapallon säde [km]
    dLat = math.radians(kaupunki1.lat - kaupunki2.lat)
    dLon = math.radians(kaupunki1.lon - kaupunki2.lon)

    lat1 = math.radians(kaupunki1.lat)
    lat2 = math.radians(kaupunki2.lat)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
        math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    etaisyys = R * c

    return etaisyys


def calc_route(reitti):
    # Laskeen kaupunkien läpi kuljetun reitin annetussa järjestyksessä.
    # - reitin tulee olla taulukko/tuple, jonka alkioina on Kaupunkeja.
    # - palautetaan kokonaismatka [km]
    kokonaismatka = 0
    for i in range(len(reitti) - 1):
        kokonaismatka += calc_distance(reitti[i], reitti[i + 1])
    return kokonaismatka


def get_cities() -> Iterable[City]:
    # Etsitään maapallon suurimpien kaupungin nimet ja koordinaatit ja järjestetään
    # suuruusjärjestykseen suurimmasta alkaen. Lähdetiedosto kopioitu sivulta:
    # https://simplemaps.com/data/world-cities 29.8.2019

    cities = list()
    with open('worldcities.csv', 'r', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_city = City(
                name=row["city"],
                pop=int(row["population"].split(".")[0] or 0),
                lat=float(row["lat"]),
                lon=float(row["lng"]),
            )
            cities.append(new_city)

    cities.sort(key=lambda x: x.pop, reverse=True)
    return cities


def main(n_cities):
    # Määritetään, minkä kaupunkien läpi joulupukki kulkee - tässä tilanteessa
    # valitsemme, että suurimpien kaupunkien. Koska tekniikka vaatii paljon
    # laskentatehoa, en suosittele yli 10 kaupungin laskemista.
    kaupungit = get_cities()
    top_largest_cities = kaupungit[0:n_cities]
    print(f"suurimmat kaupungit ovat (n={n_cities}):")
    for x in top_largest_cities:
        print(x.name, x.pop)

    # Koska joulupukki asuu Korvatunturilla, lisätään se lähtöpisteeksi.
    # Muiden kaupunkien läpi käydään reitti kaikkien reittipermutaatioiden
    # läpi ja etsitään, mikä on lyhin reitti. Permutaatiot kuvaavat kaikkia
    # erilaisia reittejä siten, että samassa kaupungissa ei pysähdytä kahdesti.
    print("*************************")
    print("== ALOITETAAN LASKENTA ==")
    print("*************************")

    min_distance = None
    min_route = None
    korvatunturi = City.Korvatunturi()

    for reitti in permutations(top_largest_cities):
        matka = calc_route((korvatunturi,) + reitti)
        min_distance = float("Inf")
        if matka < min_distance:
            min_distance = matka
            min_route = (korvatunturi,) + reitti

    print("==========================")
    print("Pienin matka on:")
    print(min_distance)
    print("========================== \n")
    print("Reitti")

    headers = {"name": "Kaupunki", "pop": "asukasluku", "lat": "latitude", "lon": "longitude"}
    printable_res = [x.__dict__ for x in min_route]
    print(tabulate(printable_res, headers=headers, tablefmt="rst"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cities", dest="cities", type=int, default=8,
                        help='max cities (tip: 10 is plenty), default=8')
    args = parser.parse_args()
    main(n_cities=args.cities)
