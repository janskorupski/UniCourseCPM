import numpy as np
import Player


class VirtualEnvironment:

    def __init__(self, players):
        self.players = players  # for now this should always be a list of length 1 with one object of type Player

    def calculate_step(self):
        # use the physics engine for one smallest time step
        pass

    def calculate_full_simulation(self):
        # use self.calculate_step and player.get_motor_output in a loop until some conditions are met
        pass

    def calculate_reward(self) -> float:
        pass

    def get_sensory_data(self) -> np.ndarray:
        pass

    def plot_game_state(self):
        pass