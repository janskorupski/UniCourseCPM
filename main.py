import time
import pygad
from new_virt_env import *
import Net

# PARAMETERS
#  SCRIPT PARAMETERS:

filename = None # if supplied, ga will continue learning from the supplied save
save_solutions = True  # this is passed to the GA instance

display_results = False  # after each generation, a random parent will be shown

# time management
time_of_learning = 60*5  # the GA will do as many generations as it can within the given time
break_time = 60*30  # due to fear of killing my weak laptop, I will give it breaks to cool down
time_between_breaks = 60*60*1.5

number_of_trials = 4  # number of games played to evaluate fitness

#  GA PARAMETERS:
num_generations = 1  # 1 is enough, since this learning will be repeated multiple times
num_parents_mating = 5

sol_per_pop = 10
num_genes = 900  # number of parameters to be used in the Players' neural networks

init_range_low = -0.5
init_range_high = 0.5

parent_selection_type = "sss"

keep_parents = 1  # doesn't do anything if keep_elitism != 0
keep_elitism = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10


def fitness_function(ga_instance, parameters, solution_idx):
    overall_fitness = 0
    for trial in range(number_of_trials):
        net_player = Net.Net(parameters)

        # the seed is calculated as any function of the parameters and trial to enable replicating and viewing
        env = VirtualEnvironment([net_player], seed=np.sum(parameters) + trial)
        env.calculate_full_simulation()
        env.fitness_function()
        overall_fitness += net_player.fitness

    print(f"gen:{ga_instance.generations_completed} sol:{solution_idx} fit:{overall_fitness/number_of_trials}")
    return overall_fitness/number_of_trials


def view_player(parameters):
    if type(parameters) is not np.ndarray:
        parameters = np.array(parameters)

    overall_fitness = 0
    for trial in range(number_of_trials):
        net_player = Net.Net(parameters)

        # the seed is calculated as any function of the parameters and trial to enable replicating and viewing
        env = VirtualEnvironment([net_player], game_mode=True, seed=np.sum(parameters) + trial)
        env.calculate_full_simulation()
        env.fitness_function()
        overall_fitness += net_player.fitness
        print(f"fitness in trial {trial} : {net_player.fitness}")

    print(f"overall fitness : {overall_fitness / number_of_trials}")


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
                           keep_elitism=keep_elitism,
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
    print(f"--- generation {ga_instance.generations_completed} ---")
    ga_instance.run()
    ga_instance.save(filename)
    print(f"--- generation avg fitness: {np.mean(ga_instance.last_generation_fitness)}")
    print(f"--- generation max fitness: {np.max(ga_instance.last_generation_fitness)}")
    if time.time() - last_break > time_between_breaks:
        time.sleep(break_time)
        last_break = time.time()

    if display_results:
        random_parent = ga_instance.last_generation_parents[np.random.randint(num_parents_mating)]
        view_player(random_parent)
