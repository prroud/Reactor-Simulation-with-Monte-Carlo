from simulation import run_monte_carlo
from plot import plot_monte_carlo_results

results = run_monte_carlo(100)

plot_monte_carlo_results(results)