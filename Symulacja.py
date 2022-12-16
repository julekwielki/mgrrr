"""
zawiera wartości prawdopodobieńst i funkcje do wyznaczania obecnego stanu każdej komórki
"""
import math
import numpy as np
import random

from komorka import Komorka


class Symulacja(object):

    def __init__(self, zdrowa, uszkodzona, zmutowana, nowotworowa, wspolne, adapt, sasiedztwo, fun_z, fun_u, fun_m,
                 fun_n, parametry, dawka):

        self.zd, self.uszk, self.zm = np.array(zdrowa), np.array(uszkodzona), np.array(zmutowana)
        self.nw, self.ws = np.array(nowotworowa), np.array(wspolne)

        self.fun_z = fun_z  # informacja czy dana funkcja jest wykorzystywana
        self.fun_u = fun_u
        self.fun_m = fun_m
        self.fun_n = fun_n
        self.nr_symulcji = parametry[4]
        self.zasieg = parametry[5]

        self.n = parametry[1] + 2  # liczba wszystkich komórek
        self.nn = parametry[0] + 1  # liczba zdrowych komórek
        self.k = parametry[2]  # liczba kroków
        self.D = 0  # dawka
        self.wiek = 1  # umownie 1 godzina
        self.alfa = parametry[3]  # 1 żeby uzyskać godziny, 60 - minuty, 3600 - sekundy

        self.xc, self.yc, self.zc = self.n // 2, self.n // 2, self.n // 2
        self.prom = parametry[0]

        self.dawka = np.ones(self.k) * parametry[6]

        if dawka:
            if len(dawka) > self.k:
                for i in range(self.k):
                    self.dawka[i] = dawka[i]
            else:
                for i in range(len(dawka)):
                    self.dawka[i] = dawka[i]

        self.zapis = [[], [], [], [], [], []]  # dane do wypisania/zapisania do pliku
        self.t = ''
        self.te = ''

        self.organizm = np.ndarray((self.n, self.n, self.n), dtype=np.object)
        self.nowe = np.empty(dtype=np.object, shape=0)
        self.nowe_xyz = []

        self.dawka_Pa = np.zeros((self.n, self.n, self.n, self.k))

        self.wykr = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]  # do wykresu

        self.zdrowe, self.uszkodzone, self.zmutowane, self.nowotworowe, self.martwe, self.pust = 0, 0, 0, 0, 0, 0
        self.zywe = 0

        """PRAWDOPODOBIEŃSTWA"""
        self.PHit, self.PD, self.PMD, self.PM, self.PR, self.PA, self.PRDEM, self.PRC = 0, 0, 0, 0, 0, 0, 0, 0
        self.PB, self.PA1, self.PDD, self.PDM, self.PRMM, self.PRD, self.PCRD = 0, 0, 0, 0, 0, 0, 0

        # stałe do odpowiedzi adaptacyjnej
        self.a1_PA = adapt[0]   # skalowanie
        self.a2_PA = adapt[1]  # a1 = 150, a2 = 15, a3 = 0.2  a/2 - dawka dla której jest maksimum - 2 jednostki
        self.a3_PA = adapt[2]  # a/2 - czas dla którego jest maksimum - 0.05714

        # wartości stałe do podziału
        if self.fun_z[1] == 1:  # podział zdrowej komórki
            self.PS = zdrowa[3] / self.alfa
        else:
            self.PS = 0
        if self.fun_u[1] == 1:  # podział uszkodzonej komórki
            self.PDS = uszkodzona[3] / self.alfa
        else:
            self.PDS = 0
        if self.fun_m[1] == 1:  # podział zmutowanej komórki
            self.PMS = zmutowana[3] / self.alfa
        else:
            self.PMS = 0
        if self.fun_n[0] == 1:  # naturalna śmierć komórki nowotworowej
            self.PCD = nowotworowa[0] / self.alfa
        else:
            self.PCD = 0
        if self.fun_n[1] == 1:  # podział komórki nowotworowej
            self.PCS = nowotworowa[1] / self.alfa
        else:
            self.PCS = 0

        self.const_PHIT = wspolne[0]  # stała do prawd. trafienia

        # stałe do smierci zdrowej komorki z przyczyn naturalnych
        self.t_PD = zdrowa[0]
        self.a_PD = zdrowa[1]
        self.n_PD = zdrowa[2]

        # stałe do śmierci uszkodzonej komórki z przyczyn naturalnych
        self.t_PDD = uszkodzona[0]
        self.a_PDD = uszkodzona[1]
        self.n_PDD = uszkodzona[2]

        # stale do smierci zmutowanej komorki z przyczyn naturalnych
        self.t_PMD = zmutowana[0]
        self.a_PMD = zmutowana[1]
        self.n_PMD = zmutowana[2]

        # stałe do spontanicznego uszkodzenia
        self.t_PM = wspolne[1]
        self.a_PM = wspolne[2]
        self.n_PM = wspolne[3]

        # stałe do transformacji w komorke nowotoworowa
        self.a_PRC = zmutowana[4]  # 0.0001 było
        self.n_PRC = zmutowana[5]

        # stałe do powstania mutacji w komórce zmutowanej
        self.a_PRMM = zmutowana[6]  # 0.0001 było

        # stałe do naprawy jednego uszkodzenia
        self.q_PR = wspolne[4]  # math.pow(10, -1.5)
        self.a_PR = wspolne[5]
        self.n_PR = wspolne[6]

        # stała do powstania uszkodzenia radiacją
        self.const_PRDEM = wspolne[7]

        # stała do transformacji komórki uszkodzonej w komorke zmutowana
        self.a_PDM = uszkodzona[4]  # 0.002 w pracy

        # stala do smierci komorki w wyniku precyzyjnego trafienia przez promieniowanie
        self.const_PRD = wspolne[8]

        # stala do smierci zwiazanej z radioczuloscia
        self.const_PCRD = nowotworowa[2]  # math.pow(10, -b) w pracy

        """EFEKT SĄSIEDZTWA"""

        self.a = sasiedztwo[0]  # szerokość komórki
        self.Mw = sasiedztwo[1]  # stała dyfuzji
        self.Malfa = sasiedztwo[2]  # stała związana z produkcją sygnałów
        self.Mbeta = sasiedztwo[3]  # sta ka rozpadu związana z redukcją liczby sygnałów
        self.Gw = sasiedztwo[4]
        self.Galfa = sasiedztwo[5]
        self.Gbeta = sasiedztwo[6]

        # stale do liczenia liczby uszkodzeń!
        self.lambdaMDP = sasiedztwo[8]  # liczba uszkodzeń powstałych na drodze MDP (przez medium)
        self.lambdaGJP = sasiedztwo[9]  # liczba uszkodzeń powstałych na drodze GJP (drogą połączeń szczelinowych)
        self.zmiana_czasu = sasiedztwo[10]

        self.roznica = 0
        self.dk = 0

    """PRAWDOPODOBIEŃSTWA"""

    def p_hit(self):  # prawdopodobienstwo trafienia komorki
        self.PHit = 1 - math.exp((-self.const_PHIT * self.D))

    def p_d(self, a, b, c):  # prawdopodobieństwo śmierci zdrowej komórki z przyczyn naturalnych
        self.PD = (1 - self.t_PD) * (
                    1 - math.exp(-self.a_PD * math.pow(self.organizm[a][b][c].wiek / self.alfa, self.n_PD))) + self.t_PD
        return self.PD

    def p_md(self, a, b, c):  # prawdopodobieństwo smierci zmutowanej komorki z przyczyn naturalnych
        self.PMD = (1 - self.t_PMD) * (
                1 - math.exp(-self.a_PMD * math.pow(self.organizm[a][b][c].wiek / self.alfa, self.n_PMD))) + self.t_PMD
        return self.PMD

    def p_dd(self, a, b, c):  # prawdopodobienstwo śmierci uszkodzonej komórki z przyczyn naturalnych
        self.PDD = (1 - self.t_PDD) * (
                1 - math.exp(-self.a_PDD * math.pow(self.organizm[a][b][c].wiek / self.alfa, self.n_PDD))) + self.t_PDD
        return self.PDD

    def p_m(self, a, b, c):  # prawdopodobienstwo spontanicznego uszkodzenia
        self.PM = (1 - self.t_PM) * (
                    1 - math.exp(-self.a_PM * math.pow(self.organizm[a][b][c].wiek / self.alfa, self.n_PM))) + self.t_PM
        return self.PM

    def p_rmm(self, a, b, c):  # prawdopodobieństwo powstania mutacji w komórce zmutowanej
        self.PRMM = 1 - math.exp(-self.a_PRMM * self.organizm[a][b][c].uszkodzenia2)
        return self.PRMM

    def p_r(self, a, b, c):  # prawdopodobieństwo naprawy jednego uszkodzenia
        self.PR = self.q_PR * math.exp(-self.a_PR * math.pow(self.organizm[a][b][c].wiek / self.alfa, self.n_PR))
        return self.PR

    def p_rdem(self):  # prawdopodobieństwo powstania uszkodzenia wywołanego radiacją
        self.PRDEM = 1 - math.exp(-self.const_PRDEM * self.D)
        return self.PRDEM

    def p_rc(self, a, b, c):  # prawdopodobieństwo transformacji w komorke nowotoworowa
        self.PRC = 1 - math.exp(-self.a_PRC * math.pow(self.organizm[a][b][c].mutacje, self.n_PRC))
        return self.PRC

    def p_dm(self, a, b, c):  # prawdopodobieństwo transformacji komórki uszkodzonej w komorke zmutowana
        self.PDM = 1 - math.exp(-self.a_PDM * self.organizm[a][b][c].uszkodzenia)  # w programie U ^ n_PDC
        return self.PDM

    def p_rd(self):  # prawdopodobieństwo smierci komorki w wyniku precyzyjnego trafienia przez promieniowanie
        self.PRD = 1 - math.exp(-self.const_PRD * self.D)
        return self.PRD

    def p_crd(self):  # prawdopodobienstwo smierci komorki nowotowrowej w zwiazku z radioczuloscia
        self.PCRD = 1 - math.exp(-self.const_PCRD * self.D)
        return self.PCRD

    """EFEKT SĄSIEDZTWA"""

    def p_b(self, a, b, c):
        self.PB = 0

        zmiana_czasu = self.zmiana_czasu

        if self.organizm[a][b][c].status != "sciana":
            self.organizm[a][b][c].stala_dyfuzji_MDP = self.Mw
        if self.organizm[a][b][c].status == "sciana":
            self.organizm[a][b][c].stala_dyfuzji_MDP = 0.0
        if self.organizm[a][b][c].status == "zdrowa" or self.organizm[a][b][c].status == "uszkodzona" or self.organizm[a][b][c].status == "zmutowana" or self.organizm[a][b][c].status == "nowotworowa":
            self.organizm[a][b][c].stala_dyfuzji_GJP = self.Gw
        if self.organizm[a][b][c].status == "martwa" or self.organizm[a][b][c].status == "pusta" or self.organizm[a][b][c].status == "sciana":
            self.organizm[a][b][c].stala_dyfuzji_GJP = 0.0

        self.organizm[a][b][c].M1 = self.Malfa * self.D - self.Mbeta * self.D + self.organizm[a][b][c].M + ((zmiana_czasu / (4.0 * self.a * self.a)) * (2.0 * (self.organizm[a + 1][b][c].stala_dyfuzji_MDP * (self.organizm[a + 1][b][c].M - self.organizm[a][b][c].M) + self.organizm[a - 1][b][c].stala_dyfuzji_MDP * (self.organizm[a - 1][b][c].M - self.organizm[a][b][c].M) + self.organizm[a][b + 1][c].stala_dyfuzji_MDP * (self.organizm[a][b + 1][c].M - self.organizm[a][b][c].M) + self.organizm[a][b - 1][c].stala_dyfuzji_MDP * (self.organizm[a][b - 1][c].M - self.organizm[a][b][c].M) + self.organizm[a][b][c + 1].stala_dyfuzji_MDP * (self.organizm[a][b][c + 1].M - self.organizm[a][b][c].M) + self.organizm[a][b][c - 1].stala_dyfuzji_MDP * (self.organizm[a][b][c - 1].M - self.organizm[a][b][c].M)) + ((self.organizm[a - 1][b - 1][c - 1].stala_dyfuzji_MDP * (self.organizm[a + 1][b][c].M - self.organizm[a][b][c].M)) + (self.organizm[a - 1][b + 1][c + 1].stala_dyfuzji_MDP * (self.organizm[a + 1][b][c].M - self.organizm[a][b][c].M)) + (self.organizm[a - 1][b - 1][c + 1].stala_dyfuzji_MDP * (self.organizm[a + 1][b][c].M - self.organizm[a][b][c].M)) + (self.organizm[a - 1][b + 1][c - 1].stala_dyfuzji_MDP * (self.organizm[a + 1][b][c].M - self.organizm[a][b][c].M)) + (self.organizm[a + 1][b - 1][c - 1].stala_dyfuzji_MDP * (self.organizm[a + 1][b][c].M - self.organizm[a][b][c].M)) + (self.organizm[a + 1][b + 1][c + 1].stala_dyfuzji_MDP * (self.organizm[a + 1][b][c].M - self.organizm[a][b][c].M)) + (self.organizm[a + 1][b - 1][c + 1].stala_dyfuzji_MDP * (self.organizm[a + 1][b][c].M - self.organizm[a][b][c].M)) + (self.organizm[a + 1][b + 1][c - 1].stala_dyfuzji_MDP * (self.organizm[a + 1][b][c].M - self.organizm[a][b][c].M)))))
        self.organizm[a][b][c].M = self.organizm[a][b][c].M1
        self.organizm[a][b][c].G1 = self.Galfa * self.D - self.Gbeta * self.D + self.organizm[a][b][c].G + ((zmiana_czasu / (4.0 * self.a * self.a)) * (2.0 * (self.organizm[a + 1][b][c].stala_dyfuzji_GJP * (self.organizm[a + 1][b][c].G - self.organizm[a][b][c].G) + self.organizm[a - 1][b][c].stala_dyfuzji_GJP * (self.organizm[a - 1][b][c].G - self.organizm[a][b][c].G) + self.organizm[a][b + 1][c].stala_dyfuzji_GJP * (self.organizm[a][b + 1][c].G - self.organizm[a][b][c].G) + self.organizm[a][b - 1][c].stala_dyfuzji_GJP * (self.organizm[a][b - 1][c].G - self.organizm[a][b][c].G) + self.organizm[a][b][c + 1].stala_dyfuzji_GJP * (self.organizm[a][b][c + 1].G - self.organizm[a][b][c].G) + self.organizm[a][b][c - 1].stala_dyfuzji_GJP * (self.organizm[a][b][c - 1].G - self.organizm[a][b][c].G)) + ((self.organizm[a - 1][b - 1][c - 1].stala_dyfuzji_GJP * (self.organizm[a + 1][b][c].G - self.organizm[a][b][c].G)) + (self.organizm[a - 1][b + 1][c + 1].stala_dyfuzji_GJP * (self.organizm[a + 1][b][c].G - self.organizm[a][b][c].G)) + (self.organizm[a - 1][b - 1][c + 1].stala_dyfuzji_GJP * (self.organizm[a + 1][b][c].G - self.organizm[a][b][c].G)) + (self.organizm[a - 1][b + 1][c - 1].stala_dyfuzji_GJP * (self.organizm[a + 1][b][c].G - self.organizm[a][b][c].G)) + (self.organizm[a + 1][b - 1][c - 1].stala_dyfuzji_GJP * (self.organizm[a + 1][b][c].G - self.organizm[a][b][c].G)) + (self.organizm[a + 1][b + 1][c + 1].stala_dyfuzji_GJP * (self.organizm[a + 1][b][c].G - self.organizm[a][b][c].G)) + (self.organizm[a + 1][b - 1][c + 1].stala_dyfuzji_GJP * (self.organizm[a + 1][b][c].G - self.organizm[a][b][c].G)) + (self.organizm[a + 1][b + 1][c - 1].stala_dyfuzji_GJP * (self.organizm[a + 1][b][c].G - self.organizm[a][b][c].G)))))
        self.organizm[a][b][c].G = self.organizm[a][b][c].G1
        self.organizm[a][b][c].uszkodzenia1 = self.organizm[a][b][c].uszkodzenia0 + self.lambdaMDP * self.organizm[a][b][c].M * zmiana_czasu + self.lambdaGJP * self.organizm[a][b][c].G * zmiana_czasu
        self.organizm[a][b][c].uszkodzenia0 = self.organizm[a][b][c].uszkodzenia1
        self.PB = self.organizm[a][b][c].uszkodzenia0
        return self.PB

    def p_a(self, x, y, z, s):  # odpowiedź adaptacyjna
        w = 0
        if int(self.organizm[x][y][z].wiek) > s:
            a = s
        else:
            a = int(self.organizm[x][y][z].wiek)

        self.PA = 0
        for i in range(a):
            w += self.wiek

            if self.dawka_Pa[x][y][z][i] > 0:
                self.dk = self.dawka_Pa[x][y][z][i]
                self.roznica = (a - i) / self.alfa
                self.PA1 = self.dk ** 2 * self.roznica ** 2 * math.exp(
                    - self.a2_PA * self.dk - self.a3_PA * self.roznica)
                self.PA = self.PA + self.PA1
        self.PA = self.PA * self.a1_PA

        return self.PA

    def widz(self, los):
        for a in range(self.n - 1):
            for b in range(self.n - 1):
                for c in range(self.n - 1):
                    self.p_b(a, b, c)
                    if los <= self.PB:
                        if self.organizm[a][b][c].status == "zdrowa":
                            self.organizm[a][b][c].uszkodzona()
                            self.organizm[a][b][c].uszkadzanie()
                        elif self.organizm[a][b][c].status == "uszkodzona":
                            self.organizm[a][b][c].uszkadzanie()
                        elif self.organizm[a][b][c].status == "zmutowana":
                            self.organizm[a][b][c].uszkadzanie()
                        else:
                            continue

    def empty(self):
        for x in range(self.n):
            for y in range(self.n):
                for z in range(self.n):
                    self.organizm[x][y][z] = Komorka()
                    self.organizm[x][y][z].wiek = 0.0
                    self.organizm[x][y][z].uszkodzenia = 0
                    self.organizm[x][y][z].status = "pusta"
                    self.organizm[x][y][z].mutacje = 0

    # """
    def ustaw_status(self, tekst):

        for x in range(self.n):  # zapełnienie komórkami
            for y in range(self.n):
                for z in range(self.n):
                    r = math.sqrt(math.pow(self.xc - x, 2) + math.pow(self.yc - y, 2) + math.pow(self.zc - z, 2))

                    if r <= self.prom:
                        self.organizm[x][y][z].status = tekst
        for x in range(self.n):
            for y in range(self.n):
                for z in range(self.n):
                    if x == 0 or y == 0 or z == 0 or x == self.n - 1 or y == self.n - 1 or z == self.n - 1:
                        self.organizm[x][y][z].status = "sciana"

    def ustaw_wczytane(self, tab):  # ustawianie statusu w przypadku gdy komórki zostały wczytane
        a = len(tab)
        if a > self.n:
            a = int(self.n)

        for x in range(a):
            for y in range(a):
                for z in range(a):
                    if tab[x][y][z].status != "sciana":
                        self.organizm[x][y][z].status = tab[x][y][z].status
                        self.organizm[x][y][z].wiek = tab[x][y][z].wiek
                        self.organizm[x][y][z].uszkodzenia = tab[x][y][z].uszkodzenia
                        self.organizm[x][y][z].mutacje = tab[x][y][z].mutacje
                        self.organizm[x][y][z].uszkodzenia2 = tab[x][y][z].uszkodzenia2
                        self.organizm[x][y][z].umieranie = tab[x][y][z].umieranie

        for x in range(self.n):
            for y in range(self.n):
                for z in range(self.n):
                    if x == 0 or y == 0 or z == 0 or x == self.n - 1 or y == self.n - 1 or z == self.n - 1:
                        self.organizm[x][y][z].status = "sciana"

    def pom(self, a, b, c, zasieg):  # zwraca położenie nowopowstałej komórki
        tab = [[], [], []]  # tab to tablica tablic zawierająca w kolejnych elementach kolejne wartości współrzędnej

        xx = range(max(a - math.ceil(self.zasieg), 0), min(self.n, a + math.ceil(self.zasieg)))
        yy = range(max(b - math.ceil(self.zasieg), 0), min(self.n, b + math.ceil(self.zasieg)))
        zz = range(max(c - math.ceil(self.zasieg), 0), min(self.n, c + math.ceil(self.zasieg)))

        for x in xx:
            for y in yy:
                for z in zz:
                    r = math.sqrt(math.pow(a - x, 2) + math.pow(b - y, 2) + math.pow(c - z, 2))
                    if r <= zasieg and self.organizm[x][y][z].zajeta != 1 and (
                            self.organizm[x][y][z].status == "pusta" or self.organizm[x][y][z].status == "martwa"):
                        tab[0].append(x)
                        tab[1].append(y)
                        tab[2].append(z)

        if len(tab[0]) != 0:  # wybiera położenie nowej komórki w sposób losowy
            nr = random.randint(0, len(tab[0]) - 1)
            return [tab[0][nr], tab[1][nr], tab[2][nr]]
        return [0, 0, 0]

    def rozmnazanie(self, a, b, c, zasieg):

        x, y, z = self.pom(a, b, c, zasieg)

        if [x, y, z] != [0, 0, 0]:
            temp = Komorka()
            temp.status = self.organizm[a][b][c].status
            temp.wiek = 0
            for s in range(self.k):
                self.dawka_Pa[x][y][z][s] = 0
            temp.uszkodzenia = self.organizm[a][b][c].uszkodzenia
            temp.uszkodzenia2 = self.organizm[a][b][c].uszkodzenia2
            temp.mutacje = self.organizm[a][b][c].mutacje
            self.organizm[x][y][z].zajeta = 1
            self.nowe = np.append(self.nowe, temp)
            self.nowe_xyz.append([x, y, z])

    def zmien_jedna(self, x, y, z, wiek, uszkodzenia, status, mutacje):
        self.organizm[x][y][z].wiek = wiek
        self.organizm[x][y][z].uszkodzenia = uszkodzenia
        self.organizm[x][y][z].status = status
        self.organizm[x][y][z].mutacje = mutacje

    def symulacja(self):

        for s in range(self.k):
            self.zdrowe, self.uszkodzone, self.zmutowane, self.nowotworowe, self.martwe, self.pust = 0, 0, 0, 0, 0, 0
            self.zywe = 0

            self.D = self.dawka[s]
            self.nowe = np.empty(dtype=np.object, shape=0)
            self.nowe_xyz = []

            for x in range(self.n):
                for y in range(self.n):
                    for z in range(self.n):
                        self.p_hit()

                        if self.organizm[x][y][z].status == "zdrowa":
                            self.organizm[x][y][z].wiek += self.wiek
                            losowa1 = random.random()
                            self.zdrowe += 1  # licznik zdrowych do wykresu
                            self.zywe += 1

                            # trafiona zdrowa komórka
                            if losowa1 <= self.PHit:
                                self.dawka_Pa[x][y][z][s] = self.D  # dawka w trafionej komórce
                                losowa2 = random.random()  # zmienna losowa do porównania z prawd.

                                self.PRD = 0 if self.fun_z[3] == 0 else self.p_rd()  # śmierć w precyzyjnym trafieniu
                                self.PD = 0 if self.fun_z[0] == 0 else self.p_d(x, y, z)  # śmierć naturalna
                                self.PM = 0 if self.fun_z[2] == 0 else self.p_m(x, y, z)  # spontaniczne uszkodzenie
                                self.PB = 0 if self.fun_z[5] == 0 else self.p_b(x, y, z)  # efekt sąsiedztwa
                                self.PRDEM = 0 if self.fun_z[4] == 0 else self.p_rdem()  # uszkodzenie radiacja

                                # śmierć komórki naturalna plus od trafienia
                                if losowa2 <= self.PD + self.PRD:
                                    self.organizm[x][y][z].martwa()

                                # uszkodzenie komórki
                                elif losowa2 <= self.PD + self.PRD + self.PM:
                                    self.organizm[x][y][z].status = "uszkodzona"
                                    self.organizm[x][y][z].uszkadzanie()

                                # naturalny podział komorki
                                elif losowa2 <= self.PD + self.PRD + self.PM + self.PS:  # rozmnażanie komórki
                                    self.rozmnazanie(x, y, z, self.zasieg)

                                # efekt widza
                                elif losowa2 <= self.PD + self.PRD + self.PM + self.PS + self.PB:
                                    self.widz(losowa2)

                                # uszkodzenie wywołane radiacją
                                elif losowa2 <= self.PD + self.PRD + self.PM + self.PS + self.PB + self.PRDEM:
                                    self.organizm[x][y][z].status = "uszkodzona"
                                    self.organizm[x][y][z].uszkadzanie()

                            # zdrowa komórka nie została trafiona
                            else:
                                self.dawka_Pa[x][y][z][s] = 0.0
                                losowa2 = random.random()

                                self.PD = 0 if self.fun_z[0] == 0 else self.p_d(x, y, z)  # śmierć naturalna
                                self.PM = 0 if self.fun_z[2] == 0 else self.p_m(x, y, z)  # spontaniczne uszkodzenie

                                # śmierć komórki
                                if losowa2 <= self.PD:
                                    self.organizm[x][y][z].martwa()

                                # spontaniczne uszkodzenie
                                elif losowa2 <= self.PD + self.PM:
                                    self.organizm[x][y][z].status = "uszkodzona"
                                    self.organizm[x][y][z].uszkadzanie()

                                # rozmnażanie
                                elif losowa2 <= self.PD + self.PM + self.PS:
                                    self.rozmnazanie(x, y, z, self.zasieg)

                        elif self.organizm[x][y][z].status == "uszkodzona":
                            self.organizm[x][y][z].wiek += self.wiek
                            losowa1 = random.random()
                            self.uszkodzone += 1
                            self.zywe += 1

                            # trafiona uszkodzona komórka
                            if losowa1 <= self.PHit:

                                self.dawka_Pa[x][y][z][s] = self.D  # dawka w trafionej komórce
                                losowa2 = random.random()  # zmienna losowa do porównania z prawd.

                                self.PDD = 0 if self.fun_u[0] == 0 else self.p_dd(x, y, z)  # przyczyny naturalne
                                self.PRD = 0 if self.fun_u[5] == 0 else self.p_rd()  # śmierć w precyzyjnym trafieniu
                                self.PM = 0 if self.fun_u[3] == 0 else self.p_m(x, y, z)  # spontaniczne uszkodzenie
                                self.PA = 0 if self.fun_u[8] == 0 else self.p_a(x, y, z, s)  # odpowiedź adaptacyjna
                                self.PR = 0 if self.fun_u[4] == 0 else self.p_r(x, y, z)  # naprawa uszkodzenia
                                self.PB = 0 if self.fun_u[7] == 0 else self.p_b(x, y, z)  # efekt widza
                                self.PRDEM = 0 if self.fun_u[6] == 0 else self.p_rdem()  # powstanie uszkodzenia
                                self.PDM = 0 if self.fun_u[2] == 0 else self.p_dm(x, y, z)  # transformacja w zmutowaną

                                # śmierć komórki
                                if losowa2 <= self.PDD + self.PRD:
                                    self.organizm[x][y][z].martwa()

                                # spontaniczne uszkodzenie
                                elif losowa2 <= self.PDD + self.PRD + self.PM:
                                    self.organizm[x][y][z].uszkadzanie()

                                # odpowiedź adaptacyjna
                                elif losowa2 <= self.PDD + self.PRD + self.PM + self.PA:
                                    if self.organizm[x][y][z].uszkodzenia == 1:
                                        self.organizm[x][y][z].status = "zdrowa"
                                        self.organizm[x][y][z].zdrowienie()
                                    else:
                                        self.organizm[x][y][z].zdrowienie()

                                # naprawa uszkodzenia naturalna
                                elif losowa2 <= self.PDD + self.PRD + self.PM + self.PA + self.PR:
                                    if self.organizm[x][y][z].uszkodzenia == 1:
                                        self.organizm[x][y][z].status = "zdrowa"
                                        self.organizm[x][y][z].zdrowienie()
                                    else:
                                        self.organizm[x][y][z].zdrowienie()

                                # rozmnażanie
                                elif losowa2 <= self.PDD + self.PRD + self.PM + self.PA + self.PR + self.PDS:
                                    self.rozmnazanie(x, y, z, self.zasieg)

                                # efekt widza
                                elif losowa2 <= self.PDD + self.PRD + self.PM + self.PA + self.PR + self.PDS + self.PB:
                                    self.widz(losowa2)

                                # dodatkowe uszkodzenie od promieniowania
                                elif losowa2 <= self.PDD + self.PRD + self.PM + self.PA + self.PR + self.PDS + self.PB + self.PRDEM:
                                    self.organizm[x][y][z].uszkadzanie()

                                # transformacja w komórkę zmutowaną
                                elif losowa2 <= self.PDD + self.PRD + self.PM + self.PA + self.PR + self.PDS + self.PB + self.PRDEM + self.PDM:
                                    self.organizm[x][y][z].status = "zmutowana"
                                    self.organizm[x][y][z].mutowanie()

                            else:
                                self.dawka_Pa[x][y][z][s] = 0.0
                                losowa2 = random.random()

                                self.PDD = 0 if self.fun_u[0] == 0 else self.p_dd(x, y, z)  # przyczyny naturalne
                                self.PM = 0 if self.fun_u[3] == 0 else self.p_m(x, y, z)  # spontaniczne uszkodzenie
                                self.PA = 0 if self.fun_u[8] == 0 else self.p_a(x, y, z, s)  # odpowiedź adaptacyjna
                                self.PR = 0 if self.fun_u[4] == 0 else self.p_r(x, y, z)  # naprawa uszkodzenia
                                self.PDM = 0 if self.fun_u[2] == 0 else self.p_dm(x, y, z)  # transformacja w zmutowaną

                                # śmierć komórki
                                if losowa2 <= self.PDD:
                                    self.organizm[x][y][z].martwa()

                                # spontaniczne uszkodzenie
                                elif losowa2 <= self.PDD + self.PM:
                                    self.organizm[x][y][z].uszkadzanie()

                                # odpowiedź adaptacyjna
                                elif losowa2 <= self.PDD + self.PM + self.PA:
                                    if self.organizm[x][y][z].uszkodzenia == 1:
                                        self.organizm[x][y][z].status = "zdrowa"
                                        self.organizm[x][y][z].zdrowienie()
                                    else:
                                        self.organizm[x][y][z].zdrowienie()

                                # naprawa uszkodzenia naturalna
                                elif losowa2 <= self.PDD + self.PM + self.PA + self.PR:
                                    if self.organizm[x][y][z].uszkodzenia == 1:
                                        self.organizm[x][y][z].status = "zdrowa"
                                        self.organizm[x][y][z].zdrowienie()
                                    else:
                                        self.organizm[x][y][z].zdrowienie()

                                # rozmnażanie
                                elif losowa2 <= self.PDD + self.PM + self.PA + self.PR + self.PDS:
                                    self.rozmnazanie(x, y, z, self.zasieg)

                                # transformacja w komórkę zmutowaną
                                elif losowa2 <= self.PDD + self.PM + self.PA + self.PR + self.PDS + self.PDM:
                                    self.organizm[x][y][z].status = "zmutowana"
                                    self.organizm[x][y][z].mutowanie()

                        elif self.organizm[x][y][z].status == "zmutowana":
                            self.organizm[x][y][z].wiek += self.wiek
                            losowa1 = random.random()
                            self.zmutowane += 1
                            self.zywe += 1

                            # trafiona zmutowana komórka
                            if losowa1 <= self.PHit:
                                self.dawka_Pa[x][y][z][s] = self.D  # dawka w trafionej komórce
                                losowa2 = random.random()  # zmienna losowa do porównania z prawd.

                                self.PMD = 0 if self.fun_m[0] == 0 else self.p_md(x, y, z)  # przyczyny naturalne
                                self.PRD = 0 if self.fun_m[5] == 0 else self.p_rd()  # śmierć w precyzyjnym trafieniu
                                self.PM = 0 if self.fun_m[3] == 0 else self.p_m(x, y, z)  # spontaniczne uszkodzenie
                                self.PB = 0 if self.fun_m[7] == 0 else self.p_b(x, y, z)  # efekt widza
                                self.PRDEM = 0 if self.fun_m[6] == 0 else self.p_rdem()  # powstanie uszkodzenia
                                self.PRC = 0 if self.fun_m[2] == 0 else self.p_rc(x, y, z)  # zamiana w nowotworową
                                self.PRMM = 0 if self.fun_m[9] == 0 else self.p_rmm(x, y, z)  # mutacja w kom zmutowanej
                                self.PR = 0 if self.fun_m[4] == 0 else self.p_r(x, y, z)  # naprawy jednego uszkodzenia
                                self.PA = 0 if self.fun_m[8] == 0 else self.p_a(x, y, z, s)  # odpowiedź adaptacyjna

                                # śmierć komórki
                                if losowa2 <= self.PMD + self.PRD:
                                    self.organizm[x][y][z].martwa()

                                # spontaniczne szkodzenie
                                elif losowa2 <= self.PMD + self.PRD + self.PM:
                                    self.organizm[x][y][z].uszkadzanie2()

                                # rozmnażanie
                                elif losowa2 <= self.PMD + self.PRD + self.PM + self.PMS:
                                    self.rozmnazanie(x, y, z, self.zasieg)

                                # efekt widza
                                elif losowa2 <= self.PMD + self.PRD + self.PM + self.PMS + self.PB:
                                    self.widz(losowa2)

                                # dodatkowe uszkodzenie od promieniowania
                                elif losowa2 <= self.PMD + self.PRD + self.PM + self.PMS + self.PB + self.PRDEM:
                                    self.organizm[x][y][z].uszkadzanie2()

                                # zmiana w nowotworową
                                elif losowa2 <= self.PMD + self.PRD + self.PM + self.PMS + self.PB + self.PRDEM + self.PRC:
                                    self.organizm[x][y][z].status = "nowotworowa"

                                # powstanie nowej mutacji
                                elif losowa2 <= self.PMD + self.PRD + self.PM + self.PMS + self.PB + self.PRDEM + self.PRC + self.PRMM:
                                    self.organizm[x][y][z].mutowanie()

                                # naprawa uszkodzenia
                                elif losowa2 <= self.PMD + self.PRD + self.PM + self.PMS + self.PB + self.PRDEM + self.PRC + self.PRMM + self.PR:
                                    if self.organizm[x][y][z].uszkodzenia2 > 0:
                                        self.organizm[x][y][z].zdrowienie2()

                                # odpowiedź adaptacyjna
                                elif losowa2 <= self.PMD + self.PRD + self.PM + self.PMS + self.PB + self.PRDEM + self.PRC + self.PRMM + self.PR + self.PA:
                                    if self.organizm[x][y][z].uszkodzenia2 > 0:
                                        self.organizm[x][y][z].zdrowienie2()

                            # nietrafiona zmutowana komórka
                            else:
                                self.dawka_Pa[x][y][z][s] = 0.0
                                losowa2 = random.random()

                                self.PMD = 0 if self.fun_m[0] == 0 else self.p_md(x, y, z)  # przyczyny naturalne
                                self.PM = 0 if self.fun_m[3] == 0 else self.p_m(x, y, z)  # spontaniczne uszkodzenie
                                self.PRC = 0 if self.fun_m[2] == 0 else self.p_rc(x, y, z)  # zamiana w nowotworową
                                self.PRMM = 0 if self.fun_m[9] == 0 else self.p_rmm(x, y, z)  # prawdopodobieństwo powstania mutacji w komórce zmutowanej
                                self.PR = 0 if self.fun_m[4] == 0 else self.p_r(x, y, z)  # prawdopodobieństwo naprawy jednego uszkodzenia
                                self.PA = 0 if self.fun_m[8] == 0 else self.p_a(x, y, z, s)  # odpowiedź adaptacyjna

                                # śmierć komórki
                                if losowa2 <= self.PMD:
                                    self.organizm[x][y][z].martwa()

                                # spontaniczne uszkodzenie
                                elif losowa2 <= self.PMD + self.PM:
                                    self.organizm[x][y][z].uszkadzanie2()

                                # podział komórki
                                elif losowa2 <= self.PMD + self.PM + self.PMS:
                                    self.rozmnazanie(x, y, z, self.zasieg)

                                # zamiana w nowotworową
                                elif losowa2 <= self.PMD + self.PM + self.PMS + self.PRC:
                                    self.organizm[x][y][z].status = "nowotworowa"

                                # powstanie nowej mutacji
                                elif losowa2 <= self.PMD + self.PM + self.PMS + self.PRC + self.PRMM:
                                    self.organizm[x][y][z].mutowanie()

                                # naprawa uszkodzenia
                                elif losowa2 <= self.PMD + self.PM + self.PMS + self.PRC + self.PRMM + self.PR:
                                    if self.organizm[x][y][z].uszkodzenia2 > 0:
                                        self.organizm[x][y][z].zdrowienie2()

                                # odpowiedź adaptacyjna
                                elif losowa2 <= self.PMD + self.PM + self.PMS + self.PRC + self.PRMM + self.PR + self.PA:
                                    if self.organizm[x][y][z].uszkodzenia2 > 0:
                                        self.organizm[x][y][z].zdrowienie2()

                        elif self.organizm[x][y][z].status == "nowotworowa":
                            self.organizm[x][y][z].wiek += self.wiek
                            losowa1 = random.random()
                            self.nowotworowe += 1
                            self.zywe += 1

                            # trafiona nowotworowa komórka
                            if losowa1 <= self.PHit:
                                self.dawka_Pa[x][y][z][s] = self.D  # dawka w trafionej komórce
                                losowa2 = random.random()  # zmienna losowa do porównania z prawd.

                                self.PRD = 0 if self.fun_n[3] == 0 else self.p_rd()  # śmierć w precyzyjnym trafieniu
                                self.PCRD = 0 if self.fun_n[2] == 0 else self.p_crd()  # smierci komorki nowotowrowej w zwiazku z radioczuloscia
                                self.PB = 0 if self.fun_n[4] == 0 else self.p_b(x, y, z)  # efekt widza

                                # śmierć komórki
                                if losowa2 <= self.PCD + self.PRD:
                                    self.organizm[x][y][z].martwa()

                                # rozmnażanie
                                elif losowa2 <= self.PCD + self.PRD + self.PCS:
                                    if self.zasieg > 3:
                                        self.rozmnazanie(x, y, z, self.zasieg - 1)
                                    else:
                                        self.rozmnazanie(x, y, z, self.zasieg)

                                # smierc z uwagi na radioczulosc
                                elif losowa2 <= self.PCD + self.PRD + self.PCS + self.PCRD:
                                    self.organizm[x][y][z].martwa()

                                # efekt widza
                                elif losowa2 <= self.PCD + self.PRD + self.PCS + self.PCRD + self.PB:
                                    self.widz(losowa2)

                            # nietrafiona nowotworowa komórka
                            else:
                                self.dawka_Pa[x][y][z][s] = 0.0
                                losowa2 = random.random()

                                # śmierć komórki
                                if losowa2 <= self.PCD:
                                    self.organizm[x][y][z].martwa()

                                # podział komórki
                                elif losowa2 <= self.PCD + self.PCS:
                                    if self.zasieg > 3:
                                        self.rozmnazanie(x, y, z, self.zasieg - 1)
                                    else:
                                        self.rozmnazanie(x, y, z, self.zasieg)

                        elif self.organizm[x][y][z].status == "martwa":
                            self.martwe += 1
                            if self.organizm[x][y][z].umieranie != 0:
                                self.organizm[x][y][z].umieranie -= 1
                            else:
                                self.organizm[x][y][z].status = "pusta"
                                self.organizm[x][y][z].zajeta = 0

                        elif self.organizm[x][y][z].status == "pusta":
                            self.pust += 1

            self.zapis[0].append(self.zdrowe)
            self.zapis[1].append(self.uszkodzone)
            self.zapis[2].append(self.zmutowane)
            self.zapis[3].append(self.nowotworowe)
            self.zapis[4].append(self.martwe)
            self.zapis[5].append(self.zywe)

            for i in range(len(self.nowe_xyz)):
                x, y, z = self.nowe_xyz[i]
                self.organizm[x][y][z] = self.nowe[i]

        self.zdrowe, self.uszkodzone, self.zmutowane, self.nowotworowe, self.martwe, self.zywe = 0, 0, 0, 0, 0, 0
        for x in range(self.n):
            for y in range(self.n):
                for z in range(self.n):
                    if self.organizm[x][y][z].status == "zdrowa":
                        self.zdrowe += 1
                        self.zywe += 1
                    elif self.organizm[x][y][z].status == "uszkodzona":
                        self.uszkodzone += 1
                        self.zywe += 1
                    elif self.organizm[x][y][z].status == "zmutowana":
                        self.zmutowane += 1
                        self.zywe += 1
                    elif self.organizm[x][y][z].status == "nowotworowa":
                        self.nowotworowe += 1
                        self.zywe += 1
                    elif self.organizm[x][y][z].status == "martwa":
                        self.martwe += 1

        self.zapis[0].append(self.zdrowe)
        self.zapis[1].append(self.uszkodzone)
        self.zapis[2].append(self.zmutowane)
        self.zapis[3].append(self.nowotworowe)
        self.zapis[4].append(self.martwe)
        self.zapis[5].append(self.zywe)

        return self.zapis, self.organizm, self.zd, self.uszk, self.zm, self.nw, self.ws, self.wykr
