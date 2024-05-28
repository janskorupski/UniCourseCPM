import time

import pygad
from new_virt_env import *
import Net
import matplotlib.pyplot as plt

# PARAMETERS
#  SCRIPT PARAMETERS:

filename = None  # if supplied, ga will continue learning from the supplied save; without the extention(!)
save_solutions = True  # this is passed to the GA instance

display_results = True  # if the best player should be displayed
teach_players = True

# time management
time_of_learning = 60*60*2  # the GA will do as many generations as it can within the given time
break_time = 60*30  # due to fear of killing my weak laptop, I will give it breaks to cool down
time_between_breaks = 60*60*1.5

number_of_trials = 4  # number of games played to evaluate fitness

#  GA PARAMETERS:
num_generations = 1  # 1 is enough, since this learning will be repeated multiple times
num_parents_mating = 5

sol_per_pop = 50
num_genes = 900  # number of parameters to be used in the Players' neural networks

init_range_low = -0.5
init_range_high = 0.5

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10

# HELP VARIABLES
i = 0
generation_number = 1  # help variable to keep track of numbers of generations
means = np.empty([])
maxes = np.empty([])


def fitness_function(ga_instance, parameters, solution_idx):
    global i
    overall_fitness = 0
    for trial in range(number_of_trials):
        player = Net.Net(parameters)
        environment = VirtualEnvironment([player])
        environment.calculate_full_simulation()
        environment.fitness_function()
        overall_fitness += player.fitness

    i += 1
    print(f"{i}/{num_generations*sol_per_pop} : {overall_fitness/number_of_trials}")
    return overall_fitness/4

if teach_players:

    if filename is None:
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
                               mutation_percent_genes=mutation_percent_genes,
                               save_solutions=save_solutions)

        filename = f"GAresults{round(random.random()*1e6)}"

    else:
        ga_instance = pygad.load(filename)


    starting_time = time.time()
    last_break = time.time()
    while time.time() - starting_time < time_of_learning:
        print(f"--- generation {generation_number} ---")
        ga_instance.run()
        ga_instance.save(filename)
        print(f"--- generation avg fitness: {np.mean(ga_instance.last_generation_fitness)}")
        np.append(means, np.mean(ga_instance.last_generation_fitness))
        np.append(maxes, np.mean(ga_instance.last_generation_fitness))

        i=0
        generation_number += 1
        if time.time() - last_break > time_between_breaks:
            time.sleep(break_time)
            last_break = time.time()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    # print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    ga_instance.plot_fitness(title="PyGAD fitness score")

if display_results:
    player = Net.Net(solution)
    environment = VirtualEnvironment([player], game_mode=True)
    environment.calculate_full_simulation()
    environment.fitness_function()

    fig = plt.figure()

    plt.plot(means, title = "mean fitness score")
    #plt.plot(maxes, title = "max fitness score")
    fig.savefig(f"{filename}_plots")