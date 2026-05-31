import numpy as np

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
    MAX_STEPS,
    P_ABSORPTION,
    P_SCATTER,
    MEAN_SECONDARY_NEUTRONS
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


def run_transport_and_reactions(initial_neutrons, nuclei):
    history = {
        "neutrons": [],
        "k_eff": [],
        "fissions": [],
        "absorptions": [],
        "scatterings": []
    }

    fissions = 0
    absorptions = 0
    scatterings = 0
    leakage = 0

    neutrons_current = initial_neutrons
    k_estimates = []

    for generation in range(MAX_STEPS):

        neutrons_next = []

        for n in neutrons_current:

            n.position = move_neutron(n.position, n.direction)

            if not is_inside_reactor(n.position):
                leakage += 1
                continue

            collided_index = check_collision(n.position, nuclei)

            if collided_index is None:
                neutrons_next.append(n)
                continue

            r = np.random.random()

            if r < P_ABSORPTION:
                absorptions += 1
                continue

            elif r < P_ABSORPTION + P_SCATTER:
                scatterings += 1
                n.direction = random_unit_vector()
                neutrons_next.append(n)
                continue

            else:
                fissions += 1

                n_new = np.random.poisson(MEAN_SECONDARY_NEUTRONS)

                for _ in range(n_new):
                    neutrons_next.append(
                        Neutron(
                            position=n.position.copy(),
                            direction=random_unit_vector()
                        )
                    )

        if len(neutrons_current) > 0:
            k_step = len(neutrons_next) / len(neutrons_current)
            k_estimates.append(k_step)

        neutrons_current = neutrons_next

        history["neutrons"].append(len(neutrons_current))
        history["k_eff"].append(k_step if len(neutrons_current) > 0 else 0)
        history["fissions"].append(fissions)
        history["absorptions"].append(absorptions)
        history["scatterings"].append(scatterings)

        if len(neutrons_current) == 0:
            print("Chain died out")
            break

    k_eff = np.mean(k_estimates) if k_estimates else 0

    return history, k_eff, fissions, absorptions, scatterings

def run_monte_carlo(n_runs = 100):
    k_values = []
    final_fissions = []
    final_absorptions = []
    final_scatterings = []

    for i in range(n_runs):
        neutrons = create_initial_neutrons()
        nuclei = create_nuclei()

        _, k_eff, f, a, s = run_transport_and_reactions(neutrons, nuclei)

        k_values.append(k_eff)
        final_fissions.append(f)
        final_absorptions.append(a)
        final_scatterings.append(s)

        print(f"Run {i}: k_eff={k_eff:.4f}, f={f}, a={a}, s={s}")
    
    results = {
        "k_eff": np.array(k_values),
        "fissions": np.array(final_fissions),
        "absorptions": np.array(final_absorptions),
        "scatterings": np.array(final_scatterings),
    }
    print("\n=== MONTE CARLO SUMMARY ===")
    print(f"Average k_eff: {results['k_eff'].mean():.4f}")
    print(f"Std k_eff: {results['k_eff'].std():.4f}")
    print(f"Runs: {n_runs}")

    return results