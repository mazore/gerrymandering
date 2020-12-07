from misc import fast_shuffle, profile
from random import random


class SwapManager:
    """Manages the swapping of two people between districts"""

    def __init__(self, canvas):
        self.canvas = canvas
        self.swaps = 0
        self.district1 = self.district2 = None
        self.person1 = self.person2 = None  # person[n] is originally from district[n]

    @profile
    def do_swap(self):
        self.get_people()

        self.person1.change_districts(self.district2)
        self.person2.change_districts(self.district1)

        if self.canvas.parameters.num_swaps_per_draw == 1:
            self.district1.draw()
            self.district2.draw()
        self.swaps += 1
        if self.swaps == self.canvas.parameters.num_swaps:
            self.canvas.rerun_simulation()

    # @profile
    def get_people(self):
        for self.district1 in fast_shuffle(self.canvas.districts):  # district1
            give_away = self.district1.ideal_give_away()
            for self.person1 in fast_shuffle(self.district1.people):  # person1
                if give_away is not None and self.person1.party != give_away:
                    continue  # if is not the ideal party to give away for this district
                if not self.person1.get_is_removable():
                    continue  # if removing will cause disconnection in district1

                if self.get_person2():
                    return
        print('no possible swaps')
        while True:  # stall
            pass

    def diff_parties_first(self, person):
        """Used in get_person2, puts people of opposite parties to person1 first (lower number)"""
        return int(person.party == self.person1.party) + random()

    # @profile
    def get_person2(self):
        for self.district2 in self.person1.get_adjacent_districts():  # district2
            district2_at_risk = 0 <= self.district2.net_advantage <= 2
            for self.person2 in sorted(self.district2.people, key=self.diff_parties_first):  # person2
                if self.district1 not in self.person2.get_adjacent_districts():
                    continue  # if not touching district1
                if district2_at_risk:  # if district2 possible to be flipped
                    party1 = self.person1.party
                    if party1 != self.canvas.parameters.advantage and party1 != self.person2.party:
                        # `return False` not `continue` to increases avg score by ~0.3 but slows down by 0.1 seconds
                        continue  # if district2 would be flipped on swap
                if self.person1 in self.person2.adjacent_people:
                    continue  # swapping two adjacent people will likely cause disconnection, although imperfect
                if not self.person2.get_is_removable():
                    continue  # if removing will cause disconnection in district2

                return True
        return False
