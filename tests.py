import atexit
from multiprocessing import Manager, Process
from parameters import Parameters
from root import Root
from simulation import BLUE


def run_process(simulation_datas, parameters, seed, testing_parameter=None):
    """Runs a process (window) and appends its simulation datas to the list"""
    root = Root(parameters=parameters, seed=seed, testing_parameter=testing_parameter)
    simulation_datas.extend(root.simulation_datas)


def get_avg_time(print_params=False, testing_parameter=None):
    """Runs simulations on one process and returns how long was spent on swapping per simulation"""
    parameters = Parameters(
        grid_width=24, district_size=16,
        num_swaps=1000, simulation_time=None, num_simulations=150,
        canvas_width=480, canvas_height=480, help_party=BLUE, favor_tie=False,
        line_width=3, sleep_between_draws=0, num_swaps_per_draw=2000,
    )
    if print_params:
        atexit.register(lambda: print(f'time parameters: {parameters}'))
    simulation_datas = []
    run_process(simulation_datas, parameters, 1, testing_parameter=testing_parameter)
    times = [simulation_data.total_swap_time for simulation_data in simulation_datas]
    return sum(times) / len(times)


def get_avg_score(print_params=False, testing_parameter=None):
    """Runs simulations on many processes and returns the average score of help_party per simulation"""
    parameters = Parameters(
        grid_width=24, district_size=16,
        num_swaps=1000, simulation_time=None, num_simulations=10,
        canvas_width=480, canvas_height=480, help_party=BLUE, favor_tie=False,
        line_width=3, sleep_between_draws=0, num_swaps_per_draw=2000,
    )
    num_processes = 50
    if print_params:
        atexit.register(lambda: print(f'score parameters: {parameters} x {num_processes} processes'))
    seeds = [i + 0 for i in range(num_processes)]  # change offset to check different seeds (shouldn't have affect)
    with Manager() as manager:
        simulation_datas = manager.list()
        processes = []
        for i in range(num_processes):
            p = Process(target=run_process, args=(simulation_datas, parameters, seeds[i], testing_parameter))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        scores = [simulation_data.score for simulation_data in simulation_datas]
        return sum(scores) / len(scores)


def black_box():
    from black_box import search_min

    def func(args):
        parameters = Parameters(
            grid_width=24, district_size=16,
            num_swaps=1000, simulation_time=None, num_simulations=150,
            canvas_width=480, canvas_height=480, help_party=BLUE, favor_tie=False,
            line_width=3, sleep_between_draws=0, num_swaps_per_draw=2000,
        )
        simulation_datas = Root(parameters=parameters, seed=1, testing_parameter=args).simulation_datas
        scores = [simulation_data.score for simulation_data in simulation_datas]
        avg_score = sum(scores) / len(scores)
        print(avg_score, args)
        return 36 - avg_score

    print(search_min(func, domain=[[0.0, 10.0]] * 25, budget=1000, batch=10, resfile='output.csv'))


def tests():
    """Prints out statistics of the project, like the avg score and time per simulation. Used to test if changes made to
    the algorithm are beneficial"""
    print(f'avg_time:  {round(get_avg_time(print_params=True) * 1000, 4)} ms')
    print(f'avg_score:  {get_avg_score(print_params=True)}')


if __name__ == '__main__':
    tests()
