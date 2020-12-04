from misc import profile
from multiprocessing import Manager, Process
from parameters import Parameters
from root import Root


class Tests:
    def __init__(self):
        self.parameters = Parameters(grid_width=24, district_size=16, num_swaps=1000)
        print(f'Grid width: {self.parameters.grid_width}')
        print(f'District size: {self.parameters.district_size}')
        print(f'Number of swaps: {self.parameters.num_swaps}')
        self.score_test()
        self.speed_test()

    def score_test(self):
        num_processes = 5  # number of processes (windows) to run simultaneously using multiprocessing
        with Manager() as manager:
            self.parameters.num_simulations = 10
            self.parameters.score_list = manager.list()
            self.parameters.avg_swap_time_list = None
            processes = []
            for i in range(num_processes):
                p = Process(target=Root.__call__, args=(self.parameters,))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
            score_list = list(self.parameters.score_list)
            print(f'Avg score ({len(score_list)} total simulations):', sum(score_list) / len(score_list))

    def speed_test(self):
        self.parameters.num_simulations = 30
        self.parameters.score_list = None  # don't need to record scores
        Root(self.parameters)
        timings = next(iter(profile.get_stats().timings.values()))
        avg_time = sum(line_timings[2] for line_timings in timings) / self.parameters.num_simulations
        avg_time *= profile.timer_unit  # scale to seconds
        print(f'do_swap avg per simulation ({self.parameters.num_simulations} simulations): ', end='')
        print(round(avg_time, 6), 'seconds')


if __name__ == '__main__':
    Tests()
