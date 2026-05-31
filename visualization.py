import pyvista as pv
import numpy as np


def visualize_history(history, reactor_radius=10, nuclei=None):

    plotter = pv.Plotter()
    plotter.set_background("black")

    # --- reactor ---
    sphere = pv.Sphere(radius=reactor_radius)
    plotter.add_mesh(sphere, style="wireframe", color="white", opacity=0.1)

    # --- nuclei ---
    if nuclei is not None:
        nuclei_pos = np.array([n.position for n in nuclei])
        plotter.add_points(nuclei_pos, color="red", point_size=6)

    positions = history["positions"]

    if len(positions) == 0:
        return

    frame = {"i": 0}

    neutrons = pv.PolyData(positions[0])
    actor = plotter.add_points(neutrons, color="cyan", point_size=5)

    txt = plotter.add_text("t=0", font_size=12)

    def update():
        i = frame["i"]

        if i >= len(positions):
            return

        pts = positions[i]

        if len(pts) > 0:
            neutrons.points = pts
            actor.mapper.SetInputData(neutrons)

        txt.SetText(0, f"generation={i}, N={len(pts)}")

        frame["i"] += 1

    # 🔥 KLUCZ: używamy timer_event (działa w starszych PyVista)
    plotter.iren.add_observer("TimerEvent", lambda obj, event: update())

    # start timer
    plotter.iren.create_timer(200)

    plotter.show()