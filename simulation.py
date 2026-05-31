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
    history = {
        "neutrons" : [],
        "nuclei": [],
        "fissions": [],
        "absorptions": [],
        "scatterings": []
    }

    fissions = 0
    absorptions = 0
    scatterings = 0

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

                reaction = handle_interaction(n, new_neutrons)

                if reaction == "fission":
                    nuclei.pop(collided_index)
                    fissions += 1

                elif reaction == "absorption":
                    absorptions += 1

                elif reaction == "scatter":
                    scatterings += 1

                n.alive = False

            else:
                new_neutrons.append(n)
        
        neutrons = new_neutrons

        history["neutrons"].append(neutrons)
        history["nuclei"].append(nuclei)
        history["fissions"].append(fissions)
        history["absorptions"].append(absorptions)
        history["scatterings"].append(scatterings)

        print(
            f"Krok {step}: "
            f"n={len(neutrons)}, "
            f"j={len(nuclei)}, "
            f"f={fissions}, "
            f"a={absorptions}, "
            f"s={scatterings}"
        )

        if len(neutrons) == 0:
            print("Reakcja wygasła")
            break
    
    return history