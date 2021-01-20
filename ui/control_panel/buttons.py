from ctypes import windll
from misc import rgb_to_hex
from ui.parameter_panel.misc import InvalidParameter
import tkinter as tk


class ButtonBase(tk.Button):
    def __init__(self, control_panel, **kwargs):
        self.root = control_panel.root
        super().__init__(control_panel, **kwargs)

        self.blue, self.blue_increasing = 0, True
        self.flashing, self.flash_id = False, None

    def update_color(self):
        factor = 1 if self.blue_increasing else -1
        self.blue += 50 * factor
        if not 0 < self.blue < 255:
            self.blue_increasing = not self.blue_increasing
        self.config(bg=rgb_to_hex(255, 255, self.blue))
        self.flash_id = self.after(50, self.update_color)

    def start_flashing(self):
        if self.flashing:
            return
        self.flashing = True
        self.update_color()

    def stop_flashing(self):
        if not self.flashing:
            return
        self.flashing = False
        self.config(bg='SystemButtonFace')
        if self.flash_id is not None:
            self.after_cancel(self.flash_id)
            self.flash_id = None


class PlayPauseButton(ButtonBase):
    def __init__(self, control_panel):
        self.root = control_panel.root
        super().__init__(control_panel, command=self.play_pause, width=5)
        self.update_config()

        self.start_flashing()

    def play_pause(self):
        """Toggle whether the simulation is playing or paused"""
        self.stop_flashing()
        if self.root.canvas.running:
            self.root.canvas.pause()  # calls self.update_config
        else:
            self.root.canvas.run()  # calls self.update_config

    def update_config(self):
        """Update the text of the button"""
        text = 'Pause' if self.root.canvas.running else 'Play'
        self.config(text=text)


class RestartButton(ButtonBase):
    def __init__(self, control_panel):
        self.root = control_panel.root
        super().__init__(control_panel, command=self.restart, text='Restart')

    def restart(self):
        self.root.focus()  # remove focus from all widgets

        errors = []
        for adjuster in self.root.parameter_panel.adjusters.values():
            value = adjuster.get()
            if isinstance(value, InvalidParameter):
                errors.append(f'{adjuster.name} {value.message.lower()}')
        if errors:  # if a parameter is invalid
            windll.user32.MessageBoxW(None, '\n'.join(errors), "Can't restart", 0)
            return  # if a parameter is invalid

        parameters = self.root.parameter_panel.get_parameters()
        self.root.parameter_panel.on_restart()
        self.root.parameters = parameters
        self.root.restart_simulation()


class SwapButton(ButtonBase):
    def __init__(self, control_panel):
        self.root = control_panel.root
        super().__init__(control_panel, command=self.swap, text='1 Swap')

    def swap(self):
        self.root.canvas.swap_manager.swap_dispatch()
        self.root.update()


class ToggleDistrictsButton(ButtonBase):
    def __init__(self, control_panel):
        self.root = control_panel.root
        # use lambda to make sure function changes when root.canvas changes
        super().__init__(control_panel, command=lambda: self.root.canvas.toggle_districts_visible())
        self.update_config()

    def update_config(self):
        """Update the text of the button"""
        show_hide = 'Hide' if self.root.canvas.show_districts else 'Show'
        self.config(text=f'{show_hide} Districts')
