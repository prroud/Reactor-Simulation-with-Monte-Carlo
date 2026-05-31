from simulation import (
    create_initial_neutrons,
    create_nuclei,
    run_transport
)

neutrons = create_initial_neutrons()
nuclei = create_nuclei()

print(f"Start: {len(neutrons)} neutronów")

neutrons = run_transport(neutrons)

print("Koniec symulacji")