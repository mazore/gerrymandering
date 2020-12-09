from misc import profile, BLUE, RED
from multiprocessing import Manager, Process
from parameters import Parameters
from root import Root


def run_process(simulation_datas, parameters, seed):
    """Runs a process (window) and appends the simulation datas to the list"""
    simulation_datas.extend(Root(parameters=parameters, seed=seed).simulation_datas)


def get_avg_time():
    """Runs simulations on one process and returns how long was spent on swapping per simulation"""
    parameters = Parameters(
        grid_width=24, district_size=16, num_swaps=1000,
        simulation_time=None, num_simulations=100,
        width=480, height=480, advantage=BLUE, disadvantage=RED,
        line_width=3, ms_between_draws=1, num_swaps_per_draw=2000,
    )
    print('time parameters: ', parameters)
    simulation_datas = []
    run_process(simulation_datas, parameters, 1)

    assert len(profile.functions) == 1 and profile.functions[0].__name__ == 'swap'
    timings = next(iter(profile.get_stats().timings.values()))
    avg_time = sum(line_timings[2] for line_timings in timings) / parameters.num_simulations
    avg_time *= profile.timer_unit  # scale to seconds
    return round(avg_time, 6)


def get_avg_score():
    """Runs simulations on many processes and returns the average score of the advantaged party per simulation"""
    parameters = Parameters(
        grid_width=24, district_size=16, num_swaps=1000,
        simulation_time=None, num_simulations=10,
        width=480, height=480, advantage=BLUE, disadvantage=RED,
        line_width=3, ms_between_draws=1, num_swaps_per_draw=2000,
    )
    num_processes = 50
    print('score parameters: ', parameters, 'x', num_processes, 'processes')
    seeds = list(range(num_processes))
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
    """Prints out statistics of the project, like the avg score and time per simulation. Used to test if changes made to
        the algorithm are beneficial"""
    avg_time = get_avg_time()
    avg_score = get_avg_score()
    print('avg_time: ', avg_time, 'seconds')
    print('avg_score: ', avg_score)


if __name__ == '__main__':
    tests()
