import numpy as np
from vispy import scene, app

from simulation import (
    create_initial_neutrons,
    create_nuclei,
    run_transport_step
)

from config import SIM_STEPS_PER_FRAME

# -------------------------
# SCENE
# -------------------------

canvas = scene.SceneCanvas(keys="interactive", show=True, bgcolor="black")
view = canvas.central_widget.add_view()
view.camera = scene.cameras.TurntableCamera(fov=45)

canvas.title = "Neutron Reactor v2 (stable + trails)"

neutron_plot = scene.visuals.Markers()
view.add(neutron_plot)

line_plot = scene.visuals.Line(color="cyan", width=1)
view.add(line_plot)

# nuclei
nuclei, _ = create_nuclei()
nuclei_pos = np.array([n.position for n in nuclei])

nuclei_plot = scene.visuals.Markers()
nuclei_plot.set_data(nuclei_pos, face_color="red", size=3)
view.add(nuclei_plot)

# -------------------------
# STATE
# -------------------------

neutrons, next_id = create_initial_neutrons()
trajectories = {}

# -------------------------
# UPDATE
# -------------------------

def update(event):

    global neutrons, next_id, trajectories

    all_positions = []

    for _ in range(SIM_STEPS_PER_FRAME):

        neutrons, next_id, positions = run_transport_step(
            neutrons,
            None,
            next_id,
            trajectories
        )

        all_positions.extend(positions)

        if len(neutrons) == 0:
            neutrons, next_id = create_initial_neutrons(next_id)

    if all_positions:
        neutron_plot.set_data(
            np.array(all_positions),
            face_color="cyan",
            size=4
        )

    all_lines = []

    for traj in trajectories.values():
        if len(traj) > 1:
            filtered = [p for p, life in traj if life > 0]

            if len(filtered) > 1:
                all_lines.append(np.array(filtered))

    if all_lines:
        line_plot.set_data(np.vstack(all_lines))


timer = app.Timer(interval=1/60, connect=update, start=True)

app.run()