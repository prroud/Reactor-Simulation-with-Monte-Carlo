from dataclasses import dataclass
import numpy as np

@dataclass
class Neutron:
    position: np.ndarray
    direction: np.ndarray
    alive: bool = True