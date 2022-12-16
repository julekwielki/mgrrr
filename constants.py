# wartości parametrów dla tkanek
import math

""" Limfocyty """

# stałe do odpowiedzi adaptacyjnej
a1_PA = 22.9   # skalowanie
a2_PA = 79.4    # 2/a - dawka dla której jest maksimum
a3_PA = 0.0832  # 2/a - czas dla którego jest maksimum - 24 h

# wartości stałe do podziału
PS = 0.0027  # podział zdrowej komórki
PDS = 0.002  # podział uszkodzonej komórki
PMS = 0.002  # podział zmutowanej komórki
PCS = 0.009  # podział komórki nowotworowej

PCD = 0.0004  # naturalna śmierć komórki nowotworowej

# napromienianie
const_PHIT = 1.3  # stała do prawd. trafienia
const_PRDEM = 2.4  # stała do powstania uszkodzenia radiacją
const_PRD = 0.5  # stala do smierci komorki w wyniku precyzyjnego trafienia przez promieniowanie

const_PCRD = 0.32  # stala do smierci zwiazanej z radioczuloscia

# stałe do smierci zdrowej komorki z przyczyn naturalnych
t_PD = 0.00035
a_PD = 2 * math.pow(10, -12)
n_PD = 3.0

# stałe do śmierci uszkodzonej komórki z przyczyn naturalnych
t_PDD = 0.00045
a_PDD = 5 * math.pow(10, -12)
n_PDD = 3.0

# stale do smierci zmutowanej komorki z przyczyn naturalnych
t_PMD = 0.004
a_PMD = 1 * math.pow(10, -10)
n_PMD = 3.0

# stałe do spontanicznego uszkodzenia
t_PM = 0.001
a_PM = 6.8 * math.pow(10, -12)
n_PM = 3.0

# stałe do naprawy jednego uszkodzenia
q_PR = 0.04
a_PR = 1 * math.pow(10, -12)
n_PR = 4.0

# stała do transformacji komórki uszkodzonej w komorke zmutowana
a_PDM = 1 * math.pow(10, -6)

# stałe do powstania mutacji w komórce zmutowanej
a_PRMM = 0.0002

# stałe do transformacji w komorke nowotoworowa
a_PRC = 2 * math.pow(10, -9)
n_PRC = 9

"""EFEKT SĄSIEDZTWA"""

a = math.pow(10, -5)  # szerokość komórki
Mw = 0.15  # stała dyfuzji
Malfa = 7  # stała związana z produkcją sygnałów
Mbeta = 0.1  # sta ka rozpadu związana z redukcją liczby sygnałów
Gw = 0.0000000005
Galfa = 1.0
Gbeta = 0.00118

# stale do liczenia liczby uszkodzeń!
lambda_D = 0.0
lambdaMDP = 0.01  # liczba uszkodzeń powstałych na drodze MDP (przez medium)
lambdaGJP = 0.01  # liczba uszkodzeń powstałych na drodze GJP (drogą połączeń szczelinowych)
zmiana_czasu = 0.1

ZDROWA_L = [t_PD, a_PD, n_PD, PS]  # śmierć, rozmnażanie
USZKODZONA_L = [t_PDD, a_PDD, n_PDD, PDS, a_PDM]  # śmierć, rozmnażanie, transformacja
ZMUTOWANA_L = [t_PMD, a_PMD, n_PMD, PMS, a_PRC, n_PRC, a_PRMM]  # śmierć, rozmnażanie, transformacja, kolejna mutacja
NOWOTWOROWA_L = [PCD, PCS, const_PCRD]  # smierc, rozmnazanie, smierc z raioczułości
WSPOLNE_L = [const_PHIT, t_PM, a_PM, n_PM, q_PR, a_PR, n_PR, const_PRDEM, const_PRD]  # traf, uszk, napr, uszk r, śmierć r
ADAPT_L = [a1_PA, a2_PA, a3_PA]
SASIEDZTWO_L = [a, Mw, Malfa, Mbeta, Gw, Galfa, Gbeta, lambda_D, lambdaMDP, lambdaGJP, zmiana_czasu]
