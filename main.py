import pygad
import VirtualEnvironment
import Net
import torchga

# use the implemented VirtualEnvironment and Player classes to find an optimal player
# this has to be done either with a Genetic Algorithm (GA) or Simulated Annealing (SA)
# below is what it could look like with GA (copied from https://pygad.readthedocs.io/en/latest/)


def fitness_function(ga_instance, parameters, solution_idx):
    player = Net.Net(parameters)
    environment = VirtualEnvironment.VirtualEnvironment([player])
    environment.calculate_full_simulation()
    fitness = environment.calculate_reward()
    return fitness


num_generations = 50
num_parents_mating = 4

sol_per_pop = 8
num_genes =  # number of parameters to be used in the Players' neural networks

init_range_low = -3
init_range_high = 3

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10

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
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
