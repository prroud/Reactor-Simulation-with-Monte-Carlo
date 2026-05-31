from simulation import (
    create_initial_neutrons,
    create_nuclei,
    run_transport_and_reactions
)

from plot import plot_history

neutrons = create_initial_neutrons()
nuclei = create_nuclei()

history = run_transport_and_reactions(neutrons, nuclei)

plot_history(history)
print("Koniec symulacji")