from .misc import TIE
from collections import defaultdict
from misc import hex_to_rgb, rgb_to_hex


class District:
    """Represents a collection of people, with a line drawn around them. The winner is determined by which party has
    the most people contained in this district"""

    def __init__(self, canvas, p1, p2):
        self.canvas = canvas

        (self.x1, self.y1), (self.x2, self.y2) = p1, p2  # In grid coordinates
        self.net_advantage = 0  # help_party score - hinder_party score
        self.people = []
        self.get_people()
        self.draw()

    def __repr__(self):
        return f'District that contains a person at {self.people[0].x, self.people[0].y} ' \
               f'won by {self.get_winner()} with +{abs(self.net_advantage)} people margin'

    def ideal_give_away(self):
        """Which party this district prioritizes giving away, in the form of a person1 swapped into district2"""
        if self.canvas.parameters.favor_tie:
            if self.tied:
                return None
            return self.get_winner()

        if -4 <= self.net_advantage <= 2:  # If not flippable or safe help_party, share our help_party people
            return self.canvas.parameters.hinder_party  # If flippable/at risk, try to get more help_party people
        return self.canvas.parameters.help_party

    def get_people(self):
        """Used only on initialization, for filling self.people list, setting up people, and setting score"""
        for grid_y in range(int(self.y1), int(self.y2)):
            for grid_x in range(int(self.x1), int(self.x2)):
                person = self.canvas.people_grid[grid_y][grid_x]

                self.people.append(person)
                person.district = self
                self.canvas.itemconfig(person.outer_id, state='normal')
                self.net_advantage += 1 if person.party == self.canvas.parameters.help_party else -1

    @property
    def tied(self):
        return self.net_advantage == 0

    def get_winner(self):
        """Get whichever party has a majority of people, or a tie"""
        if self.tied:
            return TIE
        return self.canvas.parameters.help_party if self.net_advantage > 0 else self.canvas.parameters.hinder_party

    def get_district1_weight(self):
        """Returns the weight to use for this district when picking a randomized district1. Values were determined by a
        black box optimization method"""
        if 0 < self.net_advantage <= 2:  # If at risk
            return 1
        if self.tied:
            return 11
        if -4 <= self.net_advantage <= 0:  # If flippable
            return 4.35442295
        if self.net_advantage > 2:  # If safe to help_party
            return 2.47490108
        return 2.06497273  # If safe not flippable/safe for hinder_party

    @staticmethod
    def get_district2_weight(_):
        """Returns the weight to use for this district when picking a randomized district2"""
        return 1  # To be implemented

    def draw(self):
        """Draw the outline and fill of the district"""
        # Outline
        line_ids = set()
        line_id_occurrence_map = defaultdict(int)
        for person in self.people:
            for line_id in person.edge_ids:
                line_ids.add(line_id)
                line_id_occurrence_map[line_id] += 1
        for line_id in line_ids:
            # Hide if not on edge of district (if repeated)
            state = 'hidden' if line_id_occurrence_map[line_id] > 1 else 'normal'
            if not self.canvas.show_districts:
                state = 'hidden'
            if self.canvas.line_id_state_map[line_id] != state:
                self.canvas.itemconfig(line_id, state=state)
                self.canvas.line_id_state_map[line_id] = state

        # Fill

        # Show margins in shading
        color = self.get_winner().color
        if self.canvas.parameters.show_margins:
            r, g, b = hex_to_rgb(color)
            factor = abs(self.net_advantage) / self.canvas.parameters.district_size * 3
            color = rgb_to_hex(int(r * factor), int(g * factor), int(b * factor))
        for person in self.people:
            if person.outer_color != color:
                self.canvas.itemconfig(person.outer_id, fill=color)
                person.outer_color = color
