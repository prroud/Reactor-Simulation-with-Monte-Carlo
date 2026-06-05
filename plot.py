import matplotlib.pyplot as plt
import numpy as np


def plot_monte_carlo_results(results):
    k_eff = results["k_eff"]
    k_se = results["k_se"]

    fissions = results["fissions"]
    absorptions = results["absorptions"]
    scatterings = results["scatterings"]

    runs = np.arange(len(k_eff))

    plt.figure()
    plt.hist(k_eff, bins=15, alpha=0.8)

    mean_k = k_eff.mean()

    ci_low = mean_k - 1.96 * k_eff.std()
    ci_high = mean_k + 1.96 * k_eff.std()

    plt.axvline(mean_k, linestyle="-", label="mean k_eff")
    plt.axvline(ci_low, linestyle="--", color="red", label="95% CI")
    plt.axvline(ci_high, linestyle="--", color="red")

    plt.axvline(1.0, linestyle=":", label="critical k=1")

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

    sub = np.sum(k_eff < 1)
    superc = np.sum(k_eff >= 1)

    plt.bar(["subcritical", "supercritical"], [sub, superc])
    plt.title("Reactor stability classification")
    plt.ylabel("number of runs")

    plt.show()