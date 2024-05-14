import numpy as np
import Player
import torch
import torch.nn as nn
import torch.nn.functional as F


class NeuralNet(nn.Module):
    def __init__(self):
        super(NeuralNet, self).__init__()
        self.l = nn.Sequential(
            nn.Linear(7, 14),
            nn.ReLU(),
            nn.Linear(14, 28),
            nn.ReLU(),
            nn.Linear(28, 14),
            nn.ReLU(),
            nn.Linear(14, 2)
        )


class Net(Player.Player):

    def __init__(self, parameters=None):
        # 'parameters' are the parameters of the neural network (weights and biases).
        # For every player, these parameters are fixed, as they will be generate by GA.
        super().__init__()
        self.nn=self.new_neural_network(parameters)

    def get_motor_output(self) -> np.ndarray:

        return self.nn(self.get_sensory_input())
    
    def new_neural_network(self, parameters): 
        net = NeuralNet()
        with torch.no_grad():
            net.l[0].weight = nn.Parameter(torch.tensor(parameters[0].reshape(7, 14)))
            net.l[0].bias = nn.Parameter(torch.tensor(parameters[1]))
            net.l[1].weight = nn.Parameter(torch.tensor(parameters[2].reshape(14, 28)))
            net.l[1].bias = nn.Parameter(torch.tensor(parameters[3]))
            net.l[2].weight = nn.Parameter(torch.tensor(parameters[4].reshape(28, 14)))
            net.l[2].bias = nn.Parameter(torch.tensor(parameters[5]))
            net.l[3].weight = nn.Parameter(torch.tensor(parameters[6].reshape(14, 2)))
            net.l[3].bias = nn.Parameter(torch.tensor(parameters[7]))
            print(net.l[0].weight)

        print("network", net.l[0].weight)

        return net
