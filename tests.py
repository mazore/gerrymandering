from misc import profile
from multiprocessing import Manager, Process
from parameters import Parameters
from parties import BLUE, RED
from root import Root


class Tests:
    def __init__(self):
        self.avg_time = self.get_avg_time()
        self.avg_score = self.get_avg_score()
        print('avg_time: ', self.avg_time, 'seconds')
        print('avg_score: ', self.avg_score)

    def get_avg_time(self):
        parameters = Parameters(
            grid_width=24, district_size=16, num_swaps=1000,
            simulation_time=None, num_simulations=100,
            width=480, height=480, advantage=BLUE, disadvantage=RED,
            line_width=3, ms_between_draws=1, num_swaps_per_draw=2000,
        )
        print('time parameters: ', parameters)
        self.run_process([], parameters, 1)
        assert len(profile.functions) == 1 and profile.functions[0].__name__ == 'swap'
        timings = next(iter(profile.get_stats().timings.values()))
        avg_time = sum(line_timings[2] for line_timings in timings) / parameters.num_simulations
        avg_time *= profile.timer_unit  # scale to seconds
        return round(avg_time, 6)

    def get_avg_score(self):
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
            simulation_data_list = manager.list()
            processes = []
            for i in range(num_processes):
                p = Process(target=self.run_process, args=(simulation_data_list, parameters, seeds[i]))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
            score_list = [simulation_data.score for simulation_data in simulation_data_list]
            return sum(score_list) / len(score_list)

    @staticmethod
    def run_process(simulation_data_list, parameters, seed):
        simulation_data_list.extend(Root(parameters=parameters, seed=seed).simulation_data_list)


if __name__ == '__main__':
    Tests()
