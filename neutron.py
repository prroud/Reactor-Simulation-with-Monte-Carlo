from dataclasses import dataclass
import numpy as np

@dataclass
class Neutron:
    id: int
    position: np.ndarray
    direction: np.ndarray
    alive: bool = True