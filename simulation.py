import numpy as np
from scipy.spatial import cKDTree

from neutron import Neutron
from nucleus import Nucleus

from physics import (
    random_position_in_sphere,
    random_unit_vector,
    move_neutron,
    is_inside_reactor,
    handle_interaction
)

from config import (
    INITIAL_NEUTRONS,
    NUM_NUCLEI,
    NUCLEUS_INTERACTION_RADIUS,
    MAX_NEUTRONS,
    TRAIL_LIFETIME,
    MAX_TRAIL_PER_NEUTRON
)


# -------------------------
# INIT
# -------------------------

def create_initial_neutrons(next_id=0):
    neutrons = []

    for _ in range(INITIAL_NEUTRONS):
        neutrons.append(
            Neutron(
                id=next_id,
                position=random_position_in_sphere(),
                direction=random_unit_vector()
            )
        )
        next_id += 1

    return neutrons, next_id


def create_nuclei():
    nuclei = [
        Nucleus(position=random_position_in_sphere())
        for _ in range(NUM_NUCLEI)
    ]

    tree = cKDTree(np.array([n.position for n in nuclei]))

    return nuclei, tree


# -------------------------
# STEP SIMULATION
# -------------------------

def run_transport_step(neutrons, tree, next_id, trajectories):

    new_neutrons = []
    current_positions = []

    for n in neutrons:

        n.position = move_neutron(n.position, n.direction)

        if not is_inside_reactor(n.position):
            continue

        # trajektoria (pos, life)
        traj = trajectories.setdefault(n.id, [])
        traj.append((n.position.copy(), TRAIL_LIFETIME))

        current_positions.append(n.position.copy())

        reaction, next_id = handle_interaction(
            n,
            new_neutrons,
            next_id
        )

        if reaction == "scatter":
            new_neutrons.append(n)

    # limit neutronów
    if len(new_neutrons) > MAX_NEUTRONS:
        new_neutrons = new_neutrons[:MAX_NEUTRONS]

    # wygaszanie trajektorii
    for tid in list(trajectories.keys()):
        new_traj = []

        for pos, life in trajectories[tid]:
            life -= 1
            if life > 0:
                new_traj.append((pos, life))

        trajectories[tid] = new_traj

        # limit długości
        if len(trajectories[tid]) > MAX_TRAIL_PER_NEUTRON:
            trajectories[tid] = trajectories[tid][-MAX_TRAIL_PER_NEUTRON:]

    return new_neutrons, next_id, current_positions