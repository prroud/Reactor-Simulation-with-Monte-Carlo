from simulation import (
    create_initial_neutrons,
    create_nuclei,
    run_transport_and_reactions
)

neutrons = create_initial_neutrons()
nuclei = create_nuclei()

history = run_transport_and_reactions(neutrons, nuclei)

print("Koniec symulacji")