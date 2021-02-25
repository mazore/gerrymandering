from itertools import groupby


class Person:
    """This represents one person, who gets one vote for one party. District lines are drawn around these people"""

    def __init__(self, canvas, p1, p2, x, y, party):
        self.canvas = canvas

        self.party = party
        self.x, self.y = x, y
        self.p1, self.p2 = p1, p2
        self.district = None

        self.at_west, self.at_north = self.x == 0, self.y == 0
        self.at_east = self.x == self.canvas.parameters.grid_width - 1
        self.at_south = self.y == self.canvas.parameters.grid_width - 1
        """at_[direction] - Whether person is on far [direction] of grid"""
        self.person_north = self.person_south = self.person_west = self.person_east = None
        self.person_ne = self.person_se = self.person_sw = self.person_nw = None
        """person_[direction] - The person directly to the [direction] of this person"""

        self.inner_id = self.outer_id = self.outer_color = None
        """inner - smaller colored part,  outer - bigger shaded part that's colored by district winner"""
        self.east_line_id = self.south_line_id = None
        self.adjacent_people, self.surrounding_people, self.edge_ids = [], [], []

        self.setup_graphics()

    def setup_graphics(self):
        """Used only on initialization, sets up graphics drawing"""
        (x1, y1), (x2, y2) = self.p1, self.p2
        w = (x2 - x1) * 0.175
        offset = (x2 - x1) / 2 - w
        self.inner_id = self.canvas.create_rectangle(
            x1 + offset, y1 + offset, x2 - w * 2, y2 - w * 2,
            fill=self.party.color, width=0)
        self.outer_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', stipple='gray50', width=0)
        self.canvas.itemconfig(self.outer_id, state='hidden')
        self.canvas.tag_lower(self.outer_id)  # Move below outlines
        self.outer_color = 'white'

        if self.canvas.parameters.line_width == 0:
            return  # Hide lines
        self.east_line_id = self.south_line_id = None
        if not self.at_east:
            self.east_line_id = self.canvas.create_line(x2, y1, x2, y2, fill='black',
                                                        width=self.canvas.parameters.line_width, state='hidden')
            self.canvas.line_id_state_map[self.east_line_id] = 'hidden'
        if not self.at_south:
            self.south_line_id = self.canvas.create_line(x1, y2, x2, y2, fill='black',
                                                         width=self.canvas.parameters.line_width, state='hidden')
            self.canvas.line_id_state_map[self.south_line_id] = 'hidden'

    def secondary_init(self):
        """Called after all people are initialized, stores adjacent people"""
        if not self.at_north:
            self.person_north = self.canvas.people_grid[self.y - 1][self.x]
        if not self.at_east:
            self.person_east = self.canvas.people_grid[self.y][self.x + 1]
        if not self.at_south:
            self.person_south = self.canvas.people_grid[self.y + 1][self.x]
        if not self.at_west:
            self.person_west = self.canvas.people_grid[self.y][self.x - 1]

        if not self.at_north and not self.at_east:  # Northeast
            self.person_ne = self.canvas.people_grid[self.y - 1][self.x + 1]
        if not self.at_south and not self.at_east:  # Southeast
            self.person_se = self.canvas.people_grid[self.y + 1][self.x + 1]
        if not self.at_south and not self.at_west:  # Southwest
            self.person_sw = self.canvas.people_grid[self.y + 1][self.x - 1]
        if not self.at_north and not self.at_west:  # Northwest
            self.person_nw = self.canvas.people_grid[self.y - 1][self.x - 1]

        # `filter(None.__ne__, l)` removes all occurrences of None from a list
        self.adjacent_people = list(filter(None.__ne__, [
            self.person_north, self.person_south, self.person_west, self.person_east
        ]))
        self.surrounding_people = [
            self.person_north, self.person_ne, self.person_east, self.person_se,
            self.person_south, self.person_sw, self.person_west, self.person_nw
        ]
        self.edge_ids = list(filter(None.__ne__, [
            getattr(self.person_west, 'east_line_id', None), self.east_line_id,
            getattr(self.person_north, 'south_line_id', None), self.south_line_id
        ]))
        """
        adjacent_people - up to 4 people in direct cardinal directions
        surrounding_people - always length 8, includes all people in surrounding 8 squares, None if no person
        edge_ids - up to 4 tkinter Canvas ids that correspond to lines enclosing this person, hidden or not
        """

    def __repr__(self):
        return f'{str(self.party).title()} person at {self.x, self.y}'

    def get_adjacent_districts(self):
        """Returns a list of districts neighboring this person, not including the district this is in"""
        return [person.district for person in self.adjacent_people if person.district is not self.district]

    def get_is_removable(self):
        """Returns whether the person can be removed from their district without disconnecting district

        Method: get a boolean list of whether each of the surrounding 8 people are in our district. If there are more
        than 2 'streaks' of True's (including carrying over between start and end of the list), then removing the
        square will cause a disconnected group because the surrounding squares are not connected to each other. This
        works on the assumption that there are no holes, which there aren't because all districts are the same size,
        and there are no people without a district.
        """
        bool_list = [getattr(person, 'district', None) is self.district for person in self.surrounding_people]
        num_trues = bool_list.count(True)
        for k, v in groupby(bool_list * 2):
            if k and sum(1 for _ in v) >= num_trues:
                return True
        return False

    def change_districts(self, destination):
        """Change which district this person belongs to, does not change location or party"""
        self.district.people.remove(self)
        self.district.net_advantage -= 1 if self.party == self.canvas.parameters.help_party else -1
        destination.people.append(self)
        self.district = destination
        self.district.net_advantage += 1 if self.party == self.canvas.parameters.help_party else -1
