import numpy as np
import Player

class Newb(Player.Player):

    def __init__(self, parameters=[0.1, 0.2, 0.5, 0.8, 0.5, 0.2, 0.1]):
        super().__init__()
        self.parameters = parameters

    def get_motor_output(self) -> np.ndarray:
        sensory_input = self.get_sensory_input()
        first_layer = (sensory_input*np.array([1, 0]*self.visual_resolution)*(-1) + np.array([1, 0]*self.visual_resolution))[[2*i for i in range(self.visual_resolution)]]
        rotation_neuron = np.array([0.1, 0.2, 0.3, 0.01, -0.3, -0.2, -0.1])*first_layer
        rotation_neuron = np.sum(rotation_neuron)*5
        acceleration_neuron = 1 - np.sum(np.array([0.1, 0.2, 0.5, 0.8, 0.5, 0.2, 0.1]) * first_layer)
        acceleration_neuron = max(acceleration_neuron, 0)
        acceleration_neuron = acceleration_neuron*200
        # print(f"first layer={first_layer}, rotation = {rotation_neuron}, acc = {acceleration_neuron}")
        return np.array([acceleration_neuron, rotation_neuron])
