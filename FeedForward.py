import numpy as np
import keyboard
import Player


class FedForward(Player.Player):

    def __init__(self, parameters):
        # 'parameters' are the parameters of the neural network (weights and biases).
        # For every player, these parameters are fixed, as they will be generate by GA.
        # self.nn=new_neural_network(parameters)
        super().__init__()
        self.parameters = parameters

    def sigmoid(Z):
        return 1/(1+np.exp(-Z))

    def relu(Z):
        return np.maximum(0,Z)
    
    def single_layer_forward_propagation(self, A_prev, W_curr, b_curr, activation="relu"):
        Z_curr = np.dot(W_curr, A_prev) + b_curr
        
        if activation is "relu":
            activation_func = self.relu
        elif activation is "sigmoid":
            activation_func = self.sigmoid
        else:
            raise Exception('Non-supported activation function')
            
        return activation_func(Z_curr)
        
    def full_forward_propagation(self, X, params_values, nn_architecture):
        A_curr = X
        
        for idx, layer in enumerate(nn_architecture):
            layer_idx = idx + 1
            A_prev = A_curr
            
            activ_function_curr = layer["activation"]
            W_curr = params_values["W" + str(layer_idx)]
            b_curr = params_values["b" + str(layer_idx)]
            A_curr = self.single_layer_forward_propagation(A_prev, W_curr, b_curr, activ_function_curr)
            
        return A_curr


    def get_motor_output(self) -> np.ndarray:
        # the neural networks (simply the forwards propagation)
        return np.array([int(keyboard.is_pressed("w")) * 500 - int(keyboard.is_pressed("s")) * 500,
                         int(keyboard.is_pressed("d")) * 1 - int(keyboard.is_pressed("a")) * 1])
