from misc import fast_shuffle, profile
from random import random


class RestartGettingPeopleError(Exception):
    """Raised when we encounter certain conditions when getting people, and need to redo the get_people function"""
    pass


class SwapManager:
    """Manages the swapping of two people between districts"""

    def __init__(self, canvas):
        self.canvas = canvas
        self.swaps = 0
        self.district1 = self.district2 = None
        self.person1 = self.person2 = None  # person[n] is originally from district[n]

    @profile
    def do_swap(self):
        while True:
            try:
                self.get_people()
            except RestartGettingPeopleError:
                continue
            break

        self.person1.change_districts(self.district2)
        self.person2.change_districts(self.district1)
        if self.canvas.parameters.num_swaps_per_draw == 1:
            self.district1.draw()
            self.district2.draw()
        self.swaps += 1
        if self.swaps == self.canvas.parameters.num_swaps:
            self.canvas.rerun_simulation()

    def get_people(self):
        for self.district1 in fast_shuffle(self.canvas.districts):
            give_away = self.district1.ideal_give_away()
            for self.person1 in fast_shuffle(self.district1.people):
                if give_away is not None and self.person1.party != give_away:
                    continue  # if is not the ideal party to give away for this district
                if not self.person1.get_is_removable():
                    continue  # if removing will cause disconnection in district1

                # get district2 and person2
                for self.district2 in fast_shuffle(self.person1.get_adjacent_districts()):
                    for self.person2 in sorted(self.district2.people, key=self.diff_parties_first):
                        if self.district1 not in self.person2.get_adjacent_districts():
                            continue  # if not touching district1
                        if self.person1 in self.person2.adjacent_people:
                            continue  # swapping two adjacent people will likely cause disconnection, not always
                        if not self.person2.get_is_removable():
                            continue  # if removing will cause disconnection in district2
                        if 0 <= self.district2.net_advantage <= 2:
                            if self.person1.party not in (self.canvas.parameters.advantage, self.person2.party):
                                raise RestartGettingPeopleError
                        return
                raise RestartGettingPeopleError

        print('no possible swaps')
        while True:  # stall
            pass

    def diff_parties_first(self, person):
        """Used in get_person2, puts people of opposite parties to person1 first (lower number)"""
        return int(person.party == self.person1.party) + random()
