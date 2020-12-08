from parameters import Parameters
from parties import BLUE, RED
from root import Root


def test():
    parameters = Parameters(
        grid_width=24,
        district_size=16,
        num_swaps=None,
        simulation_time=0.3,
        width=480,
        height=480,
        advantage=BLUE,
        disadvantage=RED,
        line_width=3,
        ms_between_draws=1,
        num_swaps_per_draw=2000,
        num_simulations=200,
    )
    print('parameters: ', parameters)
    simulation_data_list = Root(parameters=parameters, seed=1).simulation_data_list
    scores = [simulation_data.score for simulation_data in simulation_data_list]
    print('avg_score: ', sum(scores) / len(scores))
    num_swaps_list = [simulation_data.num_swaps for simulation_data in simulation_data_list]
    print('avg_num_swaps: ', sum(num_swaps_list) / len(num_swaps_list))


if __name__ == '__main__':
    test()
