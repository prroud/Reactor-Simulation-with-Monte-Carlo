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
    
    initial_neutrons = len(neutrons)
    produced_neutrons_total = 0

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
                    n.alive = False

                elif reaction == "absorption":
                    absorptions += 1
                    n.alive = False

                elif reaction == "scatter":
                    scatterings += 1
                    new_neutrons.append(n)
                
                if reaction in ("fission", "absorption"):
                    n.alive = False

            else:
                new_neutrons.append(n)
        produced_neutrons_total += len(new_neutrons)

        neutrons = new_neutrons

        history["neutrons"].append(len(neutrons))
        history["nuclei"].append(len(nuclei))
        history["fissions"].append(fissions)
        history["absorptions"].append(absorptions)
        history["scatterings"].append(scatterings)

        if len(neutrons) == 0:
            print("Reakcja wygasła")
            break
    
    k_eff = produced_neutrons_total / initial_neutrons
    
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