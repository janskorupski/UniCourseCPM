# Training neural networks to steer robots in 2d space

This repository contains a project for the subject 'Cognitive Procesess Modelling II'. This repository is available at github under https://github.com/janskorupski/UniCourseCPM/tree/main.

## Description

### Virtual Environment
The class  `VirtualEnvironment` implements a 2d space using the Pymunk library, generates a random map, inserts a given 'player' and a reward (an 'apple') at a random place with roughly constant distance from the player. 
The method `calculate_full_simulation` lets the simulation run for a predefined amount of in-game time, after which the fitness function of the players can be calculated.

The interaction with the environment is done by getting input sensory data from in-game sensors, reading the motor output from the player and applying physical forces corresponding to the motor output. 
Each sensor reads the distance of the closest object from the player in a specified direction as well as the type of that object (wall/ apple/ nothing).
7 sensors are placed evenly at angles from -90 to 90 degrees of the direction the player is facing.

The virtual environment also has the option to turn on the 'game mode', in which case a window is open to present the simulation real-time on the screen.

### Players
The class `Player` defines how an algorithm (or a human) interacts with the virtual environment. 
 - Players of subclass `Net` are steered by a small neural network. The parameters of the network need to be given at initialisation.
 - Players of subclass `Human` can be steered by a user using the kets 'awsd' on the keyboard.
 - Players of subclass `Noob` are steered by a tiny neural network (7 neurons, 2 layers) which has been written 'by hand'. The players are somewhat able to find the rewards. This class is for demonstration purposes only.

### Learning
The learning is done in the 'main.py' file using the Genetic Algorithm. The file has been constructed in such a way as to enable settting the algorithm to run for a prespecified amount of time and to save the results often to make sure no data is lost.
The fitness function used by the genetic algorithm creates a new player based on the parameter vector, then a new virtual environment (with a seed based on the parameter vector to enable rewatching specific runs), runs the full simulation and calculates the fitness score.

The final fitness score is defined as follows
$$S = e^{-\lambda {d \over d_{max}}} + a,$$
where $d$ is the distance from the player to the apple, $d_{max}$ is the furthest possible distance to attain, $a$ is the number of apples eaten so far and $\lambda$ is a parameter that defines how much the distance from the apple is valued. 
During our simulations $\lambda$ has been set to $3$.

### Results
The trial of every player trained in the genetic algorithm can be viewed using the function `view_player` defined in `main.p`'. 
It utilises the fact that map generation is done with the sum of the parameters of the player as a random seed and the rest of the simulation is fully deterministic.
As such the exact same map can be generated and the whole trial recalculated, only this time the enviornment is run in the 'game mode', so the trial can be viewed on the screen.

### Viewign results
After learning is done to view the results simply load a file with the results of learning

`ga_instance = pygad.load(filename)`

choose a specific parameter vector

`player = ga_instance.solutions[-1] # for the last player` 
`player = ga_instance.best_solution()[0] # for the best player`

and use the `view_player` function

`view_player(player)`


