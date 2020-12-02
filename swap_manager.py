from constants import ADVANTAGE, DISADVANTAGE, NUM_SWAPS, NUM_SWAPS_PER_DRAW
from misc import profile
from random import choice, random


class SwapManager:
    """Manages the swapping of two people between districts."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.valid_swaps = 0
        self.before_score = None
        self.district1 = self.district2 = None
        self.person1 = self.person2 = None

    @profile
    def do_swap(self):
        """Takes 2 districts that are adjacent, and switches one person from each.

        It also checks to make sure the districts are continuous (connected) after swapping, and that the swap did not
        hinder the party that we're supposed to be gerrymandering for.
        """
        before_score = dict(self.canvas.score)

        self.district1 = self.get_district1()
        self.person1 = self.get_person1()
        self.district2 = self.get_district2()
        self.person2 = self.get_person2()

        if self.person1 is None or self.person2 is None:
            self.do_swap()
            return  # no choices issue

        self.person1.change_districts(self.district2)
        self.person2.change_districts(self.district1)

        if not (self.person1.is_connected and self.person2.is_connected):
            self.person1.change_districts(self.district1)
            self.person2.change_districts(self.district2)
            self.do_swap()
            return  # not continuous issue

        self.update_district_score()
        score = self.canvas.score
        if score[ADVANTAGE] < before_score[ADVANTAGE] or score[DISADVANTAGE] > before_score[DISADVANTAGE]:
            self.update_district_score(reverse=True)
            self.person1.change_districts(self.district1)
            self.person2.change_districts(self.district2)
            self.do_swap()
            return  # not beneficial issue

        if NUM_SWAPS_PER_DRAW == 1:
            self.district1.draw()
            self.district2.draw()

        self.valid_swaps += 1
        if self.valid_swaps == NUM_SWAPS:
            print(self.canvas.score[ADVANTAGE], end=',')
            self.canvas.rerun_simulation()

    def get_district1(self):
        return choice(self.canvas.districts)

    def get_person1(self):
        for person in sorted(self.district1.people, key=lambda _: random()):
            if not person.adjacent_districts:  # if person is in the middle of district
                continue

            if person.removable:
                return person

    def get_district2(self):
        return choice(self.person1.adjacent_districts)

    def get_person2(self):
        def key(p):  # put people of opposite parties first priority
            if p.party is self.person1.party:
                return 1 + random()
            return random()

        for person in sorted(self.district2.people, key=key):
            if self.district1 not in person.adjacent_districts:  # if not touching self.district1
                continue

            if person.removable:
                return person

    def update_district_score(self, reverse=False):
        factor = -1 if reverse else 1
        self.district1.change_score(self.person1.party, -1 * factor)
        self.district1.change_score(self.person2.party, 1 * factor)
        self.district2.change_score(self.person2.party, -1 * factor)
        self.district2.change_score(self.person1.party, 1 * factor)
