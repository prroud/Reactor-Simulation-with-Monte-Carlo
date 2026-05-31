from neutron import Neutron
from nucleus import Nucleus

from physics import (
    random_position_in_sphere,
    random_unit_vector
)

from config import (
    INITIAL_NEUTRONS,
    NUM_NUCLEI
)

def create_initial_neutrons():
    neutrons = []

    for _ in range(INITIAL_NEUTRONS):
        neutrons.append(
            Neutron(
                position = random_position_in_sphere,
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