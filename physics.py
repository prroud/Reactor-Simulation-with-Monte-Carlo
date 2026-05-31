import numpy as np
from config import (
    REACTOR_RADIUS,
    MEAN_FREE_PATH
)


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


