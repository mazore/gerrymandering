from misc import fast_shuffled, weighted_choice
from random import random
from time import time


class RestartGettingPeopleError(Exception):
    """Raised when we encounter certain conditions when getting people, and need to redo the getting people"""
    pass


class SwapManager:
    """Manages the swapping of two people between districts. See readme for more information on how this works"""

    def __init__(self, canvas):
        self.canvas = canvas
        self.swaps_done = 0
        self.district1 = self.district2 = None
        self.person1 = self.person2 = None  # person[n] is originally from district[n]

    def swap_dispatch(self):
        """Called every ms_between_draws (while running), calls swap multiple times if needed, draws once"""
        to_draw = set()
        for _ in range(self.canvas.parameters.num_swaps_per_draw):
            self.swap()
            to_draw.add(self.district1)
            to_draw.add(self.district2)
            simulation_time = self.canvas.parameters.simulation_time
            time_up = simulation_time is not None and time() - self.canvas.start_time >= simulation_time
            if self.swaps_done == self.canvas.parameters.num_swaps or time_up:
                self.canvas.root.rerun_simulation()
                return
        for district in to_draw:
            district.draw()

    def swap(self):
        """Do a swap of two people between their districts. See readme for more information on how this works"""
        time_before = time()

        while True:
            try:
                self.get_person1()
                self.get_person2()
                break
            except RestartGettingPeopleError:
                pass

        self.person1.change_districts(self.district2)
        self.person2.change_districts(self.district1)
        self.swaps_done += 1
        self.canvas.total_swap_time += time() - time_before

    def get_person1(self):
        """Gets district1 and person1, using with conditions to make sure no disconnections or harmful swaps occur"""
        for self.district1 in self.district1_generator():
            ideal_party1 = self.district1.ideal_give_away()

            for self.person1 in fast_shuffled(self.district1.people):
                if self.person1.party != ideal_party1:
                    continue  # if is not the ideal party to give away for this district
                if not self.person1.get_is_removable():
                    continue  # if removing will cause disconnection in district1

                return

    def get_person2(self):
        """Gets district2 and person2. If no suitable district2 is found, we raise RestartGettingPeopleError"""
        for self.district2 in fast_shuffled(self.person1.get_adjacent_districts()):
            party2_can_be_help_party = self.party2_can_be_help_party()

            for self.person2 in sorted(self.district2.people, key=self.diff_parties_first):
                if self.district1 not in self.person2.get_adjacent_districts():
                    continue  # if not touching district1
                if self.person1 in self.person2.adjacent_people:
                    continue  # swapping two adjacent people will likely cause disconnection, not always though
                if not self.person2.get_is_removable():
                    continue  # if removing will cause disconnection in district2
                if not party2_can_be_help_party and self.person2.party == self.canvas.parameters.help_party:
                    raise RestartGettingPeopleError  # better than `continue`

                return
        raise RestartGettingPeopleError

    def diff_parties_first(self, person):
        """Used in get_person2, puts people of opposite parties to person1 first (lower number)"""
        return int(person.party == self.person1.party) + random()

    def party2_can_be_help_party(self):
        """Returns person2 can be help_party without having a decrease in help_party's total score"""
        if self.person1.party != self.canvas.parameters.hinder_party:
            return True  # if net_advantages will stay the same or district2's will increase
        # now we know that district2 net_advantage is decreasing by 2 and district1 net_advantage is increasing by 2
        if self.district2.net_advantage == 2:  # if district2 will become tie from help_party
            if self.district1.net_advantage == 0:  # district1 will become help_party from tie
                return True
            else:
                return False
        elif 0 <= self.district2.net_advantage <= 1:  # if district2 will become hinder_party from help_party/tie
            if -2 <= self.district1.net_advantage <= -1:  # if district1 will become help_party/tie from hinder_party
                return True
            else:
                return False
        return True

    def district1_generator(self):
        """Yields district1 options back weighted by districts swap_order_weight"""
        district_weight_map = {d: d.get_swap_order_weight() for d in self.canvas.districts}
        while True:
            choice = weighted_choice(district_weight_map.items())
            yield choice
            del district_weight_map[choice]
