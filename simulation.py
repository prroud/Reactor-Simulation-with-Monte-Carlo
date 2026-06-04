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
    MAX_TRAIL_PER_NEUTRON,
    MAX_STEPS
)


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


def run_transport_step(neutrons, tree, next_id, trajectories):

    new_neutrons = []
    current_positions = []

    fissions = 0
    absorptions = 0
    scatterings = 0

    for n in neutrons:

        n.position = move_neutron(n.position, n.direction)

        if not is_inside_reactor(n.position):
            continue

        traj = trajectories.setdefault(n.id, [])
        traj.append((n.position.copy(), TRAIL_LIFETIME))

        current_positions.append(n.position.copy())

        hits = tree.query_ball_point(n.position, r=NUCLEUS_INTERACTION_RADIUS)

        if len(hits) == 0:
            new_neutrons.append(n)
            continue

        reaction, next_id = handle_interaction(n, new_neutrons, next_id)

        if reaction == "fission":
            fissions += 1
        elif reaction == "absorption":
            absorptions += 1
        elif reaction == "scatter":
            scatterings += 1
            new_neutrons.append(n)

    if len(new_neutrons) > MAX_NEUTRONS:
        new_neutrons = new_neutrons[:MAX_NEUTRONS]

    for tid in list(trajectories.keys()):
        new_traj = []

        for pos, life in trajectories[tid]:
            life -= 1
            if life > 0:
                new_traj.append((pos, life))

        trajectories[tid] = new_traj

        if len(trajectories[tid]) > MAX_TRAIL_PER_NEUTRON:
            trajectories[tid] = trajectories[tid][-MAX_TRAIL_PER_NEUTRON:]

    return new_neutrons, next_id, current_positions, fissions, absorptions, scatterings


def run_single_simulation():

    neutrons, next_id = create_initial_neutrons()
    nuclei, tree = create_nuclei()

    trajectories = {}

    k_estimates = []

    total_fissions = 0
    total_absorptions = 0
    total_scatterings = 0

    for _ in range(MAX_STEPS):

        neutrons, next_id, _, f, a, s = run_transport_step(
            neutrons,
            tree,
            next_id,
            trajectories
        )

        total_fissions += f
        total_absorptions += a
        total_scatterings += s

        if len(neutrons) > 0:
            k_estimates.append(len(neutrons))

        if len(neutrons) == 0:
            break

    k_estimates = np.array(k_estimates)

    if len(k_estimates) > 0:
        k_mean = np.mean(k_estimates)
        k_std = np.std(k_estimates)
        k_se = k_std / np.sqrt(len(k_estimates))
    else:
        k_mean, k_std, k_se = 0.0, 0.0, 0.0

    return k_mean, k_std, k_se, total_fissions, total_absorptions, total_scatterings


def run_monte_carlo(n_runs=100):

    k_values = []
    k_stds = []
    k_ses = []

    fissions_list = []
    absorptions_list = []
    scatterings_list = []

    for i in range(n_runs):

        k_mean, k_std, k_se, f, a, s = run_single_simulation()

        k_values.append(k_mean)
        k_stds.append(k_std)
        k_ses.append(k_se)

        fissions_list.append(f)
        absorptions_list.append(a)
        scatterings_list.append(s)

        print(f"Run {i}: k_eff={k_mean:.4f}, f={f}, a={a}, s={s}")

    k_values = np.array(k_values)
    k_ses = np.array(k_ses)

    results = {
        "k_eff": k_values,
        "k_std": np.array(k_stds),
        "k_se": k_ses,
        "fissions": np.array(fissions_list),
        "absorptions": np.array(absorptions_list),
        "scatterings": np.array(scatterings_list),
    }

    print("\n=== SUMMARY ===")
    print(f"Mean k_eff: {k_values.mean():.4f}")
    print(f"Std k_eff: {k_values.std():.4f}")

    ci_low = k_values.mean() - 1.96 * k_values.std()
    ci_high = k_values.mean() + 1.96 * k_values.std()

    print(f"95% CI approximate: [{ci_low:.4f}, {ci_high:.4f}]")
    print(f"Runs: {n_runs}")

    return results