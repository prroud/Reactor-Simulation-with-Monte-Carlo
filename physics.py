import numpy as np
from config import (
    REACTOR_RADIUS,
    MEAN_FREE_PATH,
    NUCLEUS_INTERACTION_RADIUS,
    P_FISSION,
    P_ABSORPTION,
    P_SCATTER,
    MEAN_SECONDARY_NEUTRONS
)

from neutron import Neutron



def random_unit_vector() -> np.ndarray:
    vector = np.random.normal(size = 3)

    return vector / np.linalg.norm(vector)


def random_position_in_sphere(radius = REACTOR_RADIUS):
    while True:
        point = np.random.uniform(
            -radius,
            radius,
            size = 3
        )

        if np.linalg.norm(point) <= radius:
            return point
        

def move_neutron(position, direction):
    step = np.random.exponential(MEAN_FREE_PATH)

    return position + direction * step


def is_inside_reactor(position):
    return np.linalg.norm(position) <= REACTOR_RADIUS


def check_collision(neutron_pos, nuclei):
    for nucleus in nuclei:
        dist = np.linalg.norm(neutron_pos - nucleus.position)

        if dist < NUCLEUS_INTERACTION_RADIUS:
            return nucleus
    
    return None

def handle_interaction(neutron, neutrons_list):
    r = np.random.random()

    if r < P_ABSORPTION:
        neutron.alive = False
        return
    
    elif r < P_ABSORPTION + P_SCATTER:
        neutron.direction = random_unit_vector()
        return
    
    else:
        neutron.alive = False

        n_new = np.random.poisson(MEAN_SECONDARY_NEUTRONS)

        for _ in range(n_new):
            neutrons_list.append(
                Neutron(
                    position = neutron.position.copy(),
                    direction = random_unit_vector()
                )
            )


