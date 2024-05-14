import numpy as np
import Player
import torch
import torch.nn as nn
import torch.nn.functional as F


class NeuralNet(nn.Module):
    def __init__(self, layers_outline = [[14, 28],
                                         [28, 56],
                                         [56, 14],
                                         [14, 2]]):
        super(NeuralNet, self).__init__()
        self.layers_outline = layers_outline

        self.l = nn.Sequential()

        for i, layer in enumerate(self.layers_outline):
            self.l.append(nn.Linear(layer[0], layer[1]))
            self.l.append(nn.ReLU())

        self.l.pop(-1)



class Net(Player.Player):

    def __init__(self,
                 parameters=None,
                 layers_outline=[[14, 28],
                                 [28, 14],
                                 [14, 2]]
                 ):
        # 'parameters' are the parameters of the neural network (weights and biases).
        # For every player, these parameters are fixed, as they will be generate by GA.
        super().__init__()
        self.layers_outline = layers_outline
        self.net=self.new_neural_network(parameters)


    def get_motor_output(self) -> np.ndarray:

        s_input = torch.tensor(self.get_sensory_input())
        return self.net.l(s_input)

    def new_neural_network(self, parameters): 
        net = NeuralNet(self.layers_outline)

        no_of_values_taken = 0
        for i, layer in enumerate(self.layers_outline):
            no_of_weights = layer[0]*layer[1]
            no_of_biases = layer[1]

            start = no_of_values_taken
            stop = no_of_values_taken+no_of_weights

            net.l[2*i].weight = nn.Parameter(torch.tensor(
                parameters[start:stop].reshape(
                    layer[1],
                    layer[0])
            ), requires_grad=False)

            start = stop
            stop = start + no_of_biases
            no_of_values_taken = stop

            net.l[2 * i].bias = nn.Parameter(torch.tensor(
                parameters[start:stop]
            ), requires_grad=False)

        return net

if __name__ == "__main__":

    aaa = Net(parameters=np.array(list(range(30))),
              layers_outline=[[2,3],
                              [3,2]])
    print(aaa.get_motor_output())
    pass
