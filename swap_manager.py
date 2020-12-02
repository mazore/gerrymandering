from constants import ADVANTAGE, DISADVANTAGE, NUM_SWAPS, NUM_SWAPS_PER_DRAW, OUTPUT_SCORES
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
        self.district1 = self.get_district1()
        self.person1 = self.get_person1()  # person1 is originally from district1
        self.district2 = self.get_district2()
        self.person2 = self.get_person2()  # person2 is originally from district2

        if self.person1 is None or self.person2 is None:
            self.do_swap()
            return

        if self.not_beneficial():
            self.person1.change_districts(self.district1)
            self.person2.change_districts(self.district2)
            self.do_swap()
            return

        self.person1.change_districts(self.district2)
        self.person2.change_districts(self.district1)

        if not (self.person1.get_is_connected() and self.person2.get_is_connected()):
            self.person1.change_districts(self.district1)
            self.person2.change_districts(self.district2)
            self.do_swap()
            return

        self.update_district_scores()
        if NUM_SWAPS_PER_DRAW == 1:
            self.district1.draw()
            self.district2.draw()
        self.valid_swaps += 1
        if self.valid_swaps == NUM_SWAPS:
            if OUTPUT_SCORES:
                print(self.canvas.get_score()[ADVANTAGE], end=',')
            self.canvas.rerun_simulation()

    def get_district1(self):
        return choice(self.canvas.districts)

    def get_person1(self):
        for person in sorted(self.district1.people, key=lambda _: random()):  # more efficient than random.shuffle
            if not person.get_adjacent_districts():  # if person is in the middle of district
                continue

            if person.get_is_removable():
                return person

    def get_district2(self):
        return choice(self.person1.get_adjacent_districts())

    def get_person2(self):
        def key(p):  # put people of opposite parties first priority
            if p.party is self.person1.party:
                return 1 + random()
            return random()

        for person in sorted(self.district2.people, key=key):
            if self.district1 not in person.get_adjacent_districts():  # if not touching self.district1
                continue

            if person.get_is_removable():
                return person

    def not_beneficial(self):
        """Returns whether proceeding with the swap will cause a district to flip from ADVANTAGE to TIE, or TIE to
        DISADVANTAGE

        Method: if a district is getting rid of a person in the party we are trying to advantage, and taking in a person
        from the party we are trying to disadvantage, we know the net_advantage of that district will decrease by 2. If
        the districts net_advantage is <= 2, that will cause it to flip to either TIE or DISADVANTAGE.
        """
        district1_at_risk = 0 <= self.district1.net_advantage <= 2
        district2_at_risk = 0 <= self.district2.net_advantage <= 2
        if district1_at_risk and self.person1.party is ADVANTAGE and self.person2.party is DISADVANTAGE:
            return True
        if district2_at_risk and self.person2.party is ADVANTAGE and self.person1.party is DISADVANTAGE:
            return True
        return False

    def update_district_scores(self):
        self.district1.net_advantage += -1 if self.person1.party is ADVANTAGE else 1
        self.district1.net_advantage += 1 if self.person2.party is ADVANTAGE else -1
        self.district2.net_advantage += -1 if self.person2.party is ADVANTAGE else 1
        self.district2.net_advantage += 1 if self.person1.party is ADVANTAGE else -1
