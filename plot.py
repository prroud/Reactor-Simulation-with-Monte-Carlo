import matplotlib.pyplot as plt

def plot_history(history):
    steps = range(len(history["neutrons"]))

    plt.figure()
    plt.plot(steps, history["neutrons"])
    plt.title("Liczba neutronów w czasie")
    plt.xlabel("Krok symulacji")
    plt.ylabel("Neutrony")

    plt.figure()
    plt.plot(steps, history["nuclei"])
    plt.title("Liczba jąder w czasie")
    plt.xlabel("Krok symulacji")
    plt.ylabel("Jądra")

    plt.figure()
    plt.plot(steps, history["fissions"], label = "Fission")
    plt.plot(steps, history["absorptions"], label = "Absorption")
    plt.plot(steps, history["scatterings"], label = "Scattering")

    plt.title("Typy interakcji")
    plt.xlabel("Krok symulacji")
    plt.ylabel("Liczba zdarzeń")
    plt.legend()

    plt.figure()
    plt.plot(range(len(history["k_eff"])), history["k_eff"])
    plt.title("Współczynnik mnożenia")
    plt.xlabel("Krok symulacji")
    plt.ylabel("k_eff")
    plt.axhline(1.0, linestyle="--")

    plt.show()