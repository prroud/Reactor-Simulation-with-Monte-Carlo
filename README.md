# Reactor Simulator with Monte Carlo Methods

## Opis projektu

Projekt przedstawia uproszczoną, stochastyczną symulację procesu transportu neutronów w modelu reaktora jądrowego. Celem projektu jest demonstracja metod Monte Carlo w symulacji procesów losowych, a nie wierne odwzorowanie fizyki reaktorowej.

Model obejmuje:
- ruch neutronów w przestrzeni 3D,
- losowe zderzenia z jądrami atomowymi,
- procesy: rozpraszanie, absorpcja i rozszczepienie,
- estymację efektywnego współczynnika mnożenia neutronów (k_eff),
- wizualizację oraz analizę statystyczną wyników wielu symulacji.

---

## Uruchomienie projektu
### 0. Biblioteki + wersja Python
- Projekt tworzony był w Python 3.11
- Biblioteki wraz z wersjami znajdują się w pliku `requirements.txt`

### 1. Seria symulacji Monte Carlo (analiza statystyczna)
```
python main.py
```
Spowoduje to wykonanie N niezależnych symulacji, a następnie wygenerowanie statystyk oraz wykresów: 
- rozkład wartości k_eff
- przebieg k_eff w kolejnych symulacjach
- liczba reakcji:
    - fission
    - absorption
    - scattering
- klasyfikacja reaktora:
- subcritical (k < 1)
- supercritical (k ≥ 1)

### 2. Wizualizacja pojedynczej symulacji 3D
```
python vispy_engine.py
```
Otwiera to interaktywną wizualizację 3D procesu transportu neutronów w czasie rzeczywistym.

(lewy przycisk myszy + ruch myszą = zmiana pozycji kamery 
\
scroll = przybliżanie / oddalanie)

**Uwaga!**
\
Ze względów wydajnościowych rysowana jest tylko część trajektorii

**Opis wizualizacji**

🔴 Czerwone punkty - jądra atomowe - miejsca potencjalnych interakcji neutronów
\
🔵 Niebieskie trajektorie - ślady ruchu neutronów w czasie (historia ich ruchu w przestrzeni)

## Struktura projektu
`main.py`

Plik startowy dla analizy Monte Carlo:
- uruchamia run_monte_carlo(n)
- wykonuje serię niezależnych symulacji
- generuje wykresy wyników

`simulation.py`

Główny silnik symulacji:
- inicjalizacja neutronów i jąder
- wykonanie kroków transportu neutronów
- obsługa reakcji fizycznych (fission, absorption, scatter)
- agregacja wyników jednej i wielu symulacji

`physics.py`

Warstwa fizyczna modelu:
- losowy ruch neutronów (eksponencjalny krok)
- generowanie kierunków (wektory jednostkowe)
- detekcja interakcji z jądrami
- obsługa reakcji:
    - absorpcja
    - rozpraszanie
    - rozszczepienie (generacja neutronów wtórnych)

`neutron.py`

Definicja obiektu neutronu:
- id – identyfikator
- position – pozycja w 3D
- direction – kierunek ruchu
- alive – status aktywności

`nucleus.py`

Definicja jądra atomowego:
- position – stała pozycja w przestrzeni

`plot.py`

Moduł analizy wyników:
- Generuje wykresy:
    - histogram rozkładu k_eff
    - przebieg k_eff w kolejnych symulacjach
    - liczba reakcji (fission / absorption / scattering)
    - liczba przypadków subkrytycznych i superkrytycznych

`vispy_engine.py`

Silnik wizualizacji 3D:
- realtime rendering neutronów i jąder
- animacja ruchu i trajektorii
- aktualizacja symulacji w czasie rzeczywistym

`config.py`

Plik konfiguracyjny parametrów modelu:

- Geometria:
    - REACTOR_RADIUS – promień reaktora (obszar symulacji)
    - NUM_NUCLEI – liczba jąder atomowych w przestrzeni
    - NUCLEUS_INTERACTION_RADIUS – promień oddziaływania neutron–jądro
- Neutrony:
    - INITIAL_NEUTRONS – liczba neutronów startowych
    - MAX_NEUTRONS – maksymalna liczba neutronów w symulacji
    - MAX_SECONDARY_NEUTRONS – limit neutronów wtórnych z jednego rozszczepienia
- Transport:
    - MEAN_FREE_PATH – średnia droga swobodna neutronu (długość kroku ruchu)
    - MAX_STEPS – maksymalna liczba kroków symulacji
- Prawdopodobieństwa reakcji:
    - P_FISSION – prawdopodobieństwo rozszczepienia
    - P_ABSORPTION – prawdopodobieństwo absorpcji neutronu
    - P_SCATTER – prawdopodobieństwo rozpraszania
- Produkcja neutronów:
    - MEAN_SECONDARY_NEUTRONS – średnia liczba neutronów wtórnych (rozkład Poissona)
- Wizualizacja:
    - TRAIL_LIFETIME – czas życia śladu neutronu
    - MAX_TRAIL_PER_NEUTRON – maksymalna długość śladu
    - SIM_STEPS_PER_FRAME – liczba kroków symulacji na klatkę animacji

Zmiana wartości parametrów prowadzi do istotnych zmian w dynamice układu oraz estymowanej wartości współczynnika mnożenia neutronów \(k_{eff}\).

