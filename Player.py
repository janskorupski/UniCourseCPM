import numpy as np


class Player:

    def __init__(self, parameters):
        # 'parameters' are the parameters of the neural network (weights and biases).
        # For every player, these parameters are fixed, as they will be generate by GA.
        pass

    def get_motor_output(self, sensory_input: np.ndarray) -> np.ndarray:
        # the neural networks (simply the forwards propagation)
        pass