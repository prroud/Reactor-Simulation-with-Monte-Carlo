import numpy as np
from config import (
    REACTOR_RADIUS,
    MEAN_FREE_PATH,
    P_ABSORPTION,
    P_SCATTER,
    MEAN_SECONDARY_NEUTRONS,
    MAX_SECONDARY_NEUTRONS
)

from neutron import Neutron


def random_unit_vector():
    v = np.random.normal(size=3)
    return v / np.linalg.norm(v)


def random_position_in_sphere(radius=REACTOR_RADIUS):
    while True:
        p = np.random.uniform(-radius, radius, size=3)
        if np.linalg.norm(p) <= radius:
            return p


def move_neutron(position, direction):
    step = np.random.exponential(MEAN_FREE_PATH)
    return position + direction * step


def is_inside_reactor(position):
    return np.linalg.norm(position) <= REACTOR_RADIUS


def handle_interaction(neutron, neutrons_list, next_id):
    r = np.random.random()

    if r < P_ABSORPTION:
        neutron.alive = False
        return "absorption", next_id

    elif r < P_ABSORPTION + P_SCATTER:
        neutron.direction = random_unit_vector()
        return "scatter", next_id

    else:
        neutron.alive = False

        n_new = np.random.poisson(MEAN_SECONDARY_NEUTRONS)
        n_new = min(n_new, MAX_SECONDARY_NEUTRONS)

        for _ in range(n_new):
            neutrons_list.append(
                Neutron(
                    id=next_id,
                    position=neutron.position.copy(),
                    direction=random_unit_vector()
                )
            )
            next_id += 1

        return "fission", next_id