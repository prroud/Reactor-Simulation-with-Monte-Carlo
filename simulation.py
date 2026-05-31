from neutron import Neutron
from nucleus import Nucleus

from physics import (
    random_position_in_sphere,
    random_unit_vector,
    move_neutron,
    is_inside_reactor,
    check_collision,
    handle_interaction
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


def run_transport_and_reactions(neutrons, nuclei):
    total_interactions = 0

    for step in range(MAX_STEPS):
        new_neutrons = []

        for n in neutrons:
            if not n.alive:
                continue
            
            n.position = move_neutron(n.position, n.direction)

            if not is_inside_reactor(n.position):
                n.alive = False
                continue
            
            collided_index = check_collision(n.position, nuclei)

            if collided_index is not None:

                handle_interaction(n, new_neutrons)

                nuclei.pop(collided_index)

                total_interactions += 1

                n.alive = False

            else:
                new_neutrons.append(n)
        
        neutrons = new_neutrons

        print(
            f"Krok {step}: "
            f"neutrony={len(neutrons)}, "
            f"jądra={len(nuclei)}, "
            f"interakcje={total_interactions}"
        )

        if len(neutrons) == 0:
            print("Reakcja wygasła")
            break
    
    return neutrons