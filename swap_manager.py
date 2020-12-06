from misc import fast_shuffle, profile
from random import random


class SwapManager:
    """Manages the swapping of two people between districts."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.valid_swaps = 0
        self.before_score = None
        self.district1 = self.district2 = None
        self.person1 = self.person2 = None  # person[n] is originally from district[n]

    @profile
    def do_swap(self):
        self.get_person1()

        self.person1.change_districts(self.district2)
        self.person2.change_districts(self.district1)

        if self.canvas.parameters.num_swaps_per_draw == 1:
            self.district1.draw()
            self.district2.draw()
        self.valid_swaps += 1
        if self.valid_swaps == self.canvas.parameters.num_swaps:
            self.canvas.rerun_simulation()

    def get_person1(self):
        for self.district1 in fast_shuffle(self.canvas.districts):
            give_away = self.district1.ideal_give_away()
            for self.person1 in fast_shuffle(self.district1.people):
                if give_away is not None and self.person1.party != give_away:
                    continue
                if not self.person1.get_is_removable():
                    continue

                if self.get_person2():
                    return
        print('no possible swaps')
        while True:  # stall
            pass

    def diff_parties_first(self, person):
        """Used in get_person2, puts people of opposite parties to person1 first (lower number)"""
        return int(person.party == self.person1.party) + random()

    def get_person2(self):
        for self.district2 in self.person1.get_adjacent_districts():
            for self.person2 in sorted(self.district2.people, key=self.diff_parties_first):
                if self.district1 not in self.person2.get_adjacent_districts():  # if not touching district1
                    continue
                if self.person1 in self.person2.adjacent_people:
                    continue
                if not self.person2.get_is_removable():
                    continue

                if 0 <= self.district2.net_advantage <= 2:  # if district2 possible to be flipped
                    party1 = self.person1.party
                    if party1 != self.canvas.parameters.advantage and party1 != self.person2.party:
                        continue  # if district2 would be flipped on swap

                return True
        return False
