from neutron import Neutron
from nucleus import Nucleus

from physics import (
    random_position_in_sphere,
    random_unit_vector,
    move_neutron,
    is_inside_reactor
)

from config import (
    INITIAL_NEUTRONS,
    NUM_NUCLEI,
    MAX_STEPS
)


def create_initial_neutrons():
    neutrons = []

    for _ in range(INITIAL_NEUTRONS):
        neutrons.append(
            Neutron(
                position = random_position_in_sphere(),
                direction = random_unit_vector()
            )
        )
    
    return neutrons


def create_nuclei():
    nuclei = []

    for _ in range(NUM_NUCLEI):
        nuclei.append(
            Nucleus(
                position = random_position_in_sphere()
            )
        )

    return nuclei


def run_transport(neutrons):
    for step in range(MAX_STEPS):
        alive_neutrons = []

        for n in neutrons:
            if not n.alive:
                continue
            
            n.position = move_neutron(n.position, n.direction)

            if is_inside_reactor(n.position):
                alive_neutrons.append(n)
            else:
                n.alive = False
        
        neutrons = alive_neutrons

        print(f"Krok {step}: neutrony = {len(neutrons)}")

        if len(neutrons) == 0:
            print("Reakcja wygasła")
            break
    
    return neutrons