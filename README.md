# Gerrymandering
A program that draws district lines around a two-party grid of people (equal proportions for each party) in order to
give an unfair advantage to one party.

![Example  of grid after gerrymandering for blue](https://github.com/mazore/images/blob/main/GerrymanderedForBlue.png)
![Example  of grid after gerrymandering for red](https://github.com/mazore/images/blob/main/GerrymanderedForRed.png)

Above shows the same grid of people gerrymandered for blue (31-5) and gerrymandered for red (31-5)

People are smaller red or blue squares and districts are groups of people enclosed in black lines. Districts are shaded
based on winner, which is determined by which party has more people in the district.

## Usage
Download the project and run `python main.py` in the directory. Only python3.7 standard library is required.

## Testing
Run `python tests.py`. This runs two simulations, one that figures out how much time is spent doing swaps (see
[Swapping](###swapping)) called avg_time, and another that takes the average score after a certain number of swaps
called avg_score. It also prints the parameters used to run each of these simulations, set in file `tests.py`. These
results can be compared with other versions, and the most recent results for the current version are at the bottom of
this file. Keep in mind that the avg_time varies greatly different machines.

## How It Works
### Overview
First, a grid of people is generated, with parties that are randomized while ensuring that there are an equal amount of
people in each party. Districts are then drawn around those people. Districts are initially squares of size
`district_size`, which is possible because we ensure that `grid_width` and `district_width` allow this to be possible.
From there, we perform a series of swaps of people between districts. These swaps will over time give one party
(specified by `help_party`) more and more districts, without changing the people grid.

### Swapping

We pick 2 districts, `district1` and `district2` that are touching by 2 or more people. We also pick a person from each
of those districts (`person1` and `person2`), using certain conditions to ensure that the swap not hinder the wrong
party or cause disconnections in the districts. More information about these conditions can be found in `get_person1`
and `get_person2` methods in `swap_manager.py`. We can then make `person1` part of `district2`, and `person2` part of
`district1`. 

**TODO:** Add diagram

### Structure
![Structure diagram](https://github.com/mazore/images/blob/main/GerrymanderingStructure.png)

## Roadmap & Contributing

## Test results for this version
```
avg_time:  86.3503 ms
avg_score:  29.09
score parameters: Parameters(grid_width=24, district_size=16, num_swaps=1000, simulation_time=None, num_simulations=10, width=480, height=480, help_party=blue, hinder_party=red, favor_tie=False, line_width=3, sleep_between_draws=0, num_swaps_per_draw=2000) x 50 processes
time parameters: Parameters(grid_width=24, district_size=16, num_swaps=1000, simulation_time=None, num_simulations=150, width=480, height=480, help_party=blue, hinder_party=red, favor_tie=False, line_width=3, sleep_between_draws=0, num_swaps_per_draw=2000)
```
