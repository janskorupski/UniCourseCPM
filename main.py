import time

import pygad
from new_virt_env import *
import Net

# use the implemented VirtualEnvironment and Player classes to find an optimal player
# this has to be done either with a Genetic Algorithm (GA) or Simulated Annealing (SA)
# below is what it could look like with GA (copied from https://pygad.readthedocs.io/en/latest/)

number_of_trials = 4  # number of games played to evaluate fitness

time_of_learning = 60*60*7  # the GA will do as many generations as it can within the given time
break_time = 60*30  # due to fear of killing my weak laptop, I will give it breaks to cool down
time_between_breaks = 60*60*1.5

display_results = False  # if the best player should be displayed
i = 0
generation_number = 1  # help variable to keep track of numbers of generations

num_generations = 1  # 1 is enough, since this learning will be repeated multiple times
num_parents_mating = 15

sol_per_pop = 50
num_genes = 900  # number of parameters to be used in the Players' neural networks

init_range_low = -0.5
init_range_high = 0.5

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10

def fitness_function(ga_instance, parameters, solution_idx):
    global i
    player = Net.Net(parameters)
    overall_fitness = 0
    for trial in range(number_of_trials):
        environment = VirtualEnvironment([player])
        environment.calculate_full_simulation()
        environment.fitness_function()
        overall_fitness += player.fitness

    i += 1
    print(f"{i}/{num_generations*sol_per_pop} : {overall_fitness/number_of_trials}")
    return overall_fitness/4



ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes)


filename = f"GAresults{round(random.random()*1e6)}"
starting_time = time.time()
last_break = time.time()
while time.time() - starting_time < time_of_learning:
    print(f"--- generation {generation_number} ---")
    ga_instance.run()
    ga_instance.save(filename)
    print(f"--- generation avg fitness: {np.mean(ga_instance.last_generation_fitness)}")
    i=0
    generation_number += 1
    if time.time() - last_break < time_between_breaks:
        time.sleep(break_time)


solution, solution_fitness, solution_idx = ga_instance.best_solution()
# print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

if display_results:
    player = Net.Net(solution)
    environment = VirtualEnvironment([player], game_mode=True)
    environment.calculate_full_simulation()
    environment.fitness_function()
