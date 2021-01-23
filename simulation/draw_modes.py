class DrawModes:
    def __init__(self, draw_mode_manager):
        self.normal = NormalDrawMode(draw_mode_manager)
        self.margins = MarginsDrawMode(draw_mode_manager)
        self.solid = SolidDrawMode(draw_mode_manager)

    def __iter__(self):
        for mode in self.__dict__.values():
            yield mode


class DrawModeManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.draw_modes = DrawModes(self)
        self.last_mode = self.canvas.parameters.draw_mode

        self.draw_margins = False

    def switch(self, new):
        if type(self.last_mode) is not str:
            self.last_mode.switch(False)
        new.switch(True)
        self.last_mode = new
        [district.draw() for district in self.canvas.districts]

    @classmethod
    def get_info(cls):
        return '\n'.join(draw_mode.get_info() for draw_mode in DrawModes(None))


class DrawModeBase:
    def __init__(self, draw_mode_manager, name, description):
        self.draw_mode_manager = draw_mode_manager
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def get_info(self):
        return f'{self.name} - {self.description},'

    def switch(self, switching_in):
        pass


class NormalDrawMode(DrawModeBase):
    def __init__(self, draw_mode_manager):
        super().__init__(draw_mode_manager, 'normal', 'translucent districts colors based on winner')


class MarginsDrawMode(DrawModeBase):
    def __init__(self, draw_mode_manager):
        super().__init__(draw_mode_manager, 'margins', 'change saturation of colors based on how much it is won by')

    def switch(self, switching_in):
        self.draw_mode_manager.draw_margins = switching_in


class SolidDrawMode(DrawModeBase):
    def __init__(self, draw_mode_manager):
        super().__init__(draw_mode_manager, 'solid', 'opaque districts')

    def switch(self, switching_in):
        canvas = self.draw_mode_manager.canvas
        for person in canvas.iter_people():
            canvas.itemconfig(person.outer_id, stipple='' if switching_in else 'gray50')
