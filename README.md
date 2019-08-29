# Joulupukki
Joulupukin reittilaskuri (ns. kauppamatkustajan ongelma). 

Laskee lyhimmän reitin brute force-tekniikalla korvatunturilta suurimpien kaupunkien läpi. 

## Vaatimukset
Python >=3.5

## Asennus
Asennukseen riittää tabulate -kirjaston asennus. https://pypi.org/project/tabulate/
```
python -m pip install -r requirements.txt
```

## Ajo
Koodin voi suorittaa seuraavalla käskyllä (cities-argumentti valinnainen, oletus on 8).  
```
python joulupukki.py --cities 5
```
HUOM! Yli 10 kaupungin ajo luultavasti päättyy huonosti.

## DOCKER
Koodin voi ajaa myös dockerissa: https://cloud.docker.com/repository/registry-1.docker.io/juhanitakkunen/mooc-docker-joulupukki
```
docker run juhanitakkunen/mooc-docker-joulupukki
```
