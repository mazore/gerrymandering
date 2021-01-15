import tkinter as tk


class RerunButton(tk.Button):
    def __init__(self, control_panel):
        self.root = control_panel.root
        super().__init__(control_panel, command=self.rerun, text='Rerun')

    def rerun(self):
        self.root.focus()  # remove focus from all widgets
        parameters = self.root.parameter_panel.get_parameters()
        if parameters is None:
            print('at least one parameter is invalid')
            return  # if a parameter is invalid
        self.root.parameter_panel.on_rerun()
        self.root.parameters = parameters
        self.root.rerun_simulation()


class PlayPauseButton(tk.Button):
    def __init__(self, control_panel):
        self.root = control_panel.root
        super().__init__(control_panel, width=5)
        self.update_config()

    def play_pause(self):
        if self.root.canvas.running:
            self.root.canvas.pause()
        else:
            self.root.canvas.run()

    def update_config(self):
        """Update the text of the button"""
        text = 'Pause' if self.root.canvas.running else 'Play'
        self.configure(command=self.play_pause, text=text)


class SwapButton(tk.Button):
    def __init__(self, control_panel):
        self.root = control_panel.root
        super().__init__(control_panel, command=self.swap, text='1 Swap')

    def swap(self):
        self.root.canvas.swap_manager.swap_dispatch()
        self.root.update()


class ToggleDistrictsButton(tk.Button):
    def __init__(self, control_panel):
        self.root = control_panel.root
        # use lambda to make sure function changes when root.canvas changes
        super().__init__(control_panel, command=lambda: self.root.canvas.toggle_districts_visible())
        self.update_config()

    def update_config(self):
        """Update the text of the button"""
        show_hide = 'Hide' if self.root.canvas.show_districts else 'Show'
        self.configure(text=f'{show_hide} Districts')
