import tkinter as tk


class HoverInfo:
    """Shows text when mouse is hovered on given widget"""

    def __init__(self, widget, text):
        self.widget, self.text = widget, text
        self.widget.bind('<Enter>', self.showtip)
        self.widget.bind('<Leave>', self.hidetip)
        self.top_level = None

    def showtip(self, _):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.top_level = tk.Toplevel(self.widget)
        self.top_level.wm_overrideredirect(True)  # Leaves only the label and removes the app window
        self.top_level.wm_geometry(f'+{x}+{y}')
        label = tk.Label(self.top_level, text=self.text, justify='left', background="#ffffff", relief='solid',
                         borderwidth=1, wraplength=180)
        label.pack(ipadx=1)

    def hidetip(self, _=None):
        if self.top_level:
            self.top_level.destroy()
        self.top_level = None

    def delete(self):
        self.hidetip()
        self.widget.unbind('<Enter>')
        self.widget.unbind('<Leave>')


class InvalidParameter:
    def __init__(self, message):
        self.message = message


class DefaultParametersButton(tk.Button):
    """Reset all parameters to defaults set in Parameters __init__"""

    def __init__(self, button_frame):
        self.parameter_panel = button_frame.parameter_panel
        super().__init__(button_frame, command=self.reset, font='Consolas 8', text='Default')

    def reset(self):
        for adjuster in self.parameter_panel.adjusters.values():
            adjuster.reset()


class DiscardChangesButton(tk.Button):
    """Reverts parameter adjusters to the last time restart button was pressed, basically sets them to current
    parameters used by the simulation"""

    def __init__(self, button_frame):
        self.parameter_panel = button_frame.parameter_panel
        super().__init__(button_frame, command=self.reset, font='Consolas 8', text='Discard')

    def reset(self):
        for adjuster in self.parameter_panel.adjusters.values():
            adjuster.revert()


class ButtonFrame(tk.Frame):
    def __init__(self, parameter_panel):
        self.parameter_panel = parameter_panel
        super().__init__(parameter_panel)
        DefaultParametersButton(self).pack(side='left')
        DiscardChangesButton(self).pack(side='left')
