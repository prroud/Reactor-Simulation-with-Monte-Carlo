import matplotlib.pyplot as plt
import numpy as np


def plot_monte_carlo_results(results):
    k_eff = results["k_eff"]
    fissions = results["fissions"]
    absorptions = results["absorptions"]
    scatterings = results["scatterings"]

    runs = np.arange(len(k_eff))

    plt.figure()
    plt.hist(k_eff, bins=15)
    plt.axvline(1.0, linestyle="--", label="critical k=1")
    plt.title("k_eff distribution (Monte Carlo)")
    plt.xlabel("k_eff")
    plt.ylabel("frequency")
    plt.legend()
    plt.grid(True)

    plt.figure()
    plt.plot(runs, k_eff, marker="o")
    plt.axhline(1.0, linestyle="--", label="critical k=1")
    plt.title("k_eff per simulation run")
    plt.xlabel("run")
    plt.ylabel("k_eff")
    plt.legend()
    plt.grid(True)

    plt.figure()
    plt.plot(runs, fissions, label="fissions")
    plt.plot(runs, absorptions, label="absorptions")
    plt.plot(runs, scatterings, label="scatterings")
    plt.title("Reaction statistics per run")
    plt.xlabel("run")
    plt.ylabel("count")
    plt.legend()
    plt.grid(True)


    plt.figure()
    stability = np.where(k_eff < 1, "subcritical", "supercritical")

    sub = np.sum(k_eff < 1)
    superc = np.sum(k_eff >= 1)

    plt.bar(["subcritical", "supercritical"], [sub, superc])
    plt.title("Reactor stability classification")
    plt.ylabel("number of runs")

    plt.show()