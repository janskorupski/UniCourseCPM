import numpy as np
import keyboard
import Player


class Human(Player.Player):

    def __init__(self, parameters=None):
        # 'parameters' are the parameters of the neural network (weights and biases).
        # For every player, these parameters are fixed, as they will be generate by GA.
        # self.nn=new_neural_network(parameters)
        super().__init__()

    def get_motor_output(self) -> np.ndarray:
        # the neural networks (simply the forwards propagation)
        return np.array([int(keyboard.is_pressed("w"))*500,
                int(keyboard.is_pressed("a"))*1,
                int(keyboard.is_pressed("s"))*500,
                int(keyboard.is_pressed("d"))*1])