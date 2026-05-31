from simulation import (
    create_initial_neutrons,
    create_nuclei
)

neutrons = create_initial_neutrons()
nuclei = create_nuclei()

print(f"Neutrony: {len(neutrons)}")
print(f"Jądra: {len(nuclei)}")