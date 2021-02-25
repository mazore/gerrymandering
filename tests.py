import atexit
from multiprocessing import Manager, Process
from parameters import Parameters
from root import Root


def run_process(simulation_datas, parameters, seed):
    """Runs a process (window) and appends its simulation datas to the list"""
    root = Root(parameters=parameters, seed=seed)
    simulation_datas.extend(root.simulation_datas)


def get_avg_time(print_params=False):
    """Runs simulations on one process and returns how long was spent on swapping per simulation"""
    parameters = Parameters(num_swaps_per_draw=2000, num_swaps=1000, num_simulations=150, start_running=True)
    if print_params:
        atexit.register(lambda: print(f'time parameters: {parameters}'))
    simulation_datas = []
    run_process(simulation_datas, parameters, 1)
    times = [simulation_data.total_swap_time for simulation_data in simulation_datas]
    return sum(times) / len(times)


def get_avg_score(parameters=None, num_processes=50, print_params=False):
    """Runs simulations on many processes and returns the average score of help_party per simulation"""
    if parameters is None:
        parameters = Parameters(num_swaps_per_draw=2000, num_swaps=1000, num_simulations=10, start_running=True)
    if print_params:
        atexit.register(lambda: print(f'score parameters: {parameters} x {num_processes} processes'))
    seeds = [i + 0 for i in range(num_processes)]  # Change offset to check different seeds (shouldn't have affect)
    with Manager() as manager:
        simulation_datas = manager.list()
        processes = []
        for i in range(num_processes):
            p = Process(target=run_process, args=(simulation_datas, parameters, seeds[i]))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        scores = [simulation_data.score for simulation_data in simulation_datas]
        return sum(scores) / len(scores)


def tests():
    """Prints out statistics of the project, like the avg score and time per simulation. Used to test if changes made
    to the algorithm are beneficial"""
    # print(f'avg_time:  {round(get_avg_time(print_params=True) * 1000, 4)} ms')
    print(f'avg_score:  {get_avg_score(print_params=True)}')


if __name__ == '__main__':
    tests()
