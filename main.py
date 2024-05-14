import pygad
from new_virt_env import *
import Net

# use the implemented VirtualEnvironment and Player classes to find an optimal player
# this has to be done either with a Genetic Algorithm (GA) or Simulated Annealing (SA)
# below is what it could look like with GA (copied from https://pygad.readthedocs.io/en/latest/)
i = 0


num_generations = 10
num_parents_mating = 5

sol_per_pop = 12
num_genes = 900  # number of parameters to be used in the Players' neural networks

init_range_low = -0.1
init_range_high = 0.1

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10

def fitness_function(ga_instance, parameters, solution_idx):
    global i
    player = Net.Net(parameters)
    overall_fitness = 0

    environment = VirtualEnvironment([player])
    environment.calculate_full_simulation()
    environment.fitness_function()
    overall_fitness += player.fitness

    player = Net.Net(parameters)
    environment = VirtualEnvironment([player])
    environment.calculate_full_simulation()
    environment.fitness_function()
    overall_fitness += player.fitness

    player = Net.Net(parameters)
    environment = VirtualEnvironment([player])
    environment.calculate_full_simulation()
    environment.fitness_function()
    overall_fitness += player.fitness

    player = Net.Net(parameters)
    environment = VirtualEnvironment([player])
    environment.calculate_full_simulation()
    environment.fitness_function()
    overall_fitness += player.fitness

    i += 1
    print(f"{i}/{num_generations*sol_per_pop} : {overall_fitness/4}")
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

ga_instance.run()


solution, solution_fitness, solution_idx = ga_instance.best_solution()
# print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

player = Net.Net(solution)
environment = VirtualEnvironment([player], game_mode=True)
environment.calculate_full_simulation()
environment.fitness_function()
