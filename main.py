from simulation import (
    create_initial_neutrons,
    create_nuclei,
    run_transport_and_reactions,
    run_monte_carlo
)

from visualization import visualize_history

from plot import plot_monte_carlo_results

neutrons = create_initial_neutrons()
nuclei = create_nuclei()

history, k_eff, f, a, s = run_transport_and_reactions(neutrons, nuclei)

visualize_history(history, reactor_radius=10, nuclei=nuclei)