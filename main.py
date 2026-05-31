from simulation import (
    create_initial_neutrons,
    create_nuclei,
    run_transport_and_reactions,
    run_monte_carlo
)

from plot import plot_monte_carlo_results

results = run_monte_carlo(100)

plot_monte_carlo_results(results)