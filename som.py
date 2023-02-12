"""
Zadanie: Algorytm sieci samoorganizującej się.
"""
import csv
import math
import numpy


class Neuron:
    def __init__(self, dane, etykieta=None):
        self.dane = dane
        self.etykieta = etykieta

    def  __iter__(self):
        return self.dane.__iter__()

    def __str__(self):
        return "%s (%s)" % (self.etykieta, self.dane,)
    
    def odleglosc(self, sygnal):
        # odleglosc euklidesowa: sqrt((x2-x1)^2 + (y2-y1)^2)
        return math.sqrt(sum([(v1 - v2) ** 2 for v1, v2 in zip(sygnal, self.dane)]))

    def skoryguj(self, signal, waga=0.2):
        zipped = list(zip(signal, self.dane))
        korekcja = tuple(list(map(lambda t: (t[0] - t[1]) * waga, zipped)))
        self.dane = tuple(sum(t) for t in zip(self.dane, korekcja))


class SOM:
    neuronki = []

    def __init__(self, liczba_neuronow, wsp_uczenia=0.2):
        self.liczba_neuronow = liczba_neuronow
        self.wsp_ucz = wsp_uczenia
        self.wsp_ucz_s = wsp_uczenia / 10
        for i in range(self.liczba_neuronow):
            self.neuronki.append(Neuron(tuple(numpy.random.sample(2)), str(i)))

    def trening(self, dane, iteracji=100):
        for i in range(iteracji):
            for sygnal in dane:
                najblizszy = self.znajdz_najblizszy(sygnal)
                somsiady = self.znajdz_somsasiadow(neuron=najblizszy, odleglosc=(iteracji-i/iteracji))
                najblizszy.skoryguj(sygnal, waga=self.wsp_ucz)
                for somsiad in somsiady:
                    somsiad.skoryguj(sygnal, waga=self.wsp_ucz_s)
    
    def znajdz_najblizszy(self, sygnal):
        odleglosci = []
        for neuron in self.neuronki:
            odleglosci.append((neuron, neuron.odleglosc(sygnal)))
        najblizszy, _ = min(odleglosci, key=lambda x: x[1])
        return najblizszy

    def znajdz_somsasiadow(self, neuron, odleglosc):
        somsiady = []
        for n in self.neuronki:
            if n.odleglosc(neuron) < odleglosc:
                somsiady.append(n)
        return somsiady

    def oznacz(self, sygnal, etykieta):
        najblizszy = self.znajdz_najblizszy(sygnal)
        najblizszy.etykieta = etykieta


def gen_dane_treningowe(nazwa='trening.csv'):
    dane = [[*numpy.random.sample(2)] for i in range(0,100)]
    with open(nazwa, 'w') as plik:
        w = csv.DictWriter(plik, fieldnames=('Wydatki', 'Dochod'))
        w.writeheader()
        for wiersz in dane:
            w.writerow({'Wydatki': wiersz[0], 'Dochod': wiersz[1]})
    return dane


def wczytaj_dane_treningowe(nazwa='trening.csv'):
    with open(nazwa, 'r') as plik:
        dane = [[float(v) for v in wiersz.values()] for wiersz in csv.DictReader(plik)]
    return dane


def rysuj_wykres(som, title=None, filename=None):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    markers = ['o', 'd', 's']
    for neuron in som.neuronki:
        plt.scatter(*tuple(neuron.dane), marker=markers[int(neuron.etykieta)])
    plt.xlabel("Stosunek wydatków i raty do dochodu")
    plt.ylabel("Źródło dochodu")
    if title:
        plt.title(title)
    if filename:
        plt.savefig(filename)


def wczytaj_wnioski(nazwa='wnioski.csv'):
    with open(nazwa, 'r') as plik:
        dane = [wiersz for wiersz in csv.DictReader(plik)]
    return dane


def zapisz_oceny(oceny, nazwa='oceny.csv'):
    with open(nazwa, 'w') as plik:
        w = csv.DictWriter(plik, fieldnames=[*oceny[0].keys()])
        w.writeheader()
        for ocena in oceny:
            w.writerow(ocena)


def ocena_ryzyka(som):
    oceny = []
    dane = wczytaj_wnioski()
    for wniosek in dane:
        dochod, wydatki, rata, zrodlo = wniosek.values()
        wygrany = som.znajdz_najblizszy(((int(wydatki) + int(rata)) / int(dochod), int(zrodlo) / 100,))
        oceny.append({**wniosek, 'ocena': wygrany.etykieta})
    if len(oceny):
        zapisz_oceny(oceny)


if __name__ == '__main__':
    # DANE = gen_dane_treningowe()
    DANE = wczytaj_dane_treningowe()
    
    som = SOM(liczba_neuronow=2)
    rysuj_wykres(som, "Inicjacja sieci: %s" % len(som.neuronki), 'som_init.png')
    som.trening(dane=DANE, iteracji=10000)
    rysuj_wykres(som, "Sieć po treningu: %s" % len(som.neuronki), 'som_trening.png')

    som.oznacz((0.10, 1), "ZGODA")
    som.oznacz((1, 0), "ODMOWA")

    ocena_ryzyka(som)
