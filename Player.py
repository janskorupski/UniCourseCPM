import numpy as np
import pymunk


class Player:

    def __init__(self, parameters=None):
        # 'parameters' are the parameters of the neural network (weights and biases).
        # For every player, these parameters are fixed, as they will be generate by GA.
        # self.nn=new_neural_network(parameters)

        self.points=0

        # PYMUNK SETTINGS
        radius = 30
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)

        self.shape = pymunk.Circle(self.body, radius)
        self.shape.friction = 0.1

    def get_motor_output(self, sensory_input: np.ndarray) -> np.ndarray:
        # the neural networks (simply the forwards propagation)
        pass