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

    def __init__(self, liczba_neuronow, waga=0.2):
        self.liczba_neuronow = liczba_neuronow
        self.waga = waga
        for i in range(self.liczba_neuronow):
            self.neuronki.append(Neuron(tuple(numpy.random.sample(2)), str(i)))
        
    def trening(self, dane, iteracji=100):
        for i in range(iteracji):
            for sygnal in dane:
                najblizszy = self.znajdz_najblizszy(sygnal)
                najblizszy.skoryguj(sygnal, waga=self.waga)
    
    def znajdz_najblizszy(self, sygnal):
        odleglosci = []
        for neuron in self.neuronki:
            odleglosci.append((neuron, neuron.odleglosc(sygnal)))
        najblizszy, _ = min(odleglosci, key=lambda x: x[1])
        return najblizszy

    def oznacz(self, sygnal, etykieta):
        najblizszy = self.znajdz_najblizszy(sygnal)
        najblizszy.etykieta = etykieta




