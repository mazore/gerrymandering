import tkinter as tk


class ChoicePicker(tk.OptionMenu):
    """An adjuster type that can be used to select an item from a list of (or function that returns) choices"""
    def __init__(self, container, default, choices=None, get_choices=None, after_select=None, result_formatter=None):
        if choices is not None:
            self.get_choices = lambda: choices
        elif get_choices is not None:
            self.get_choices = get_choices
        else:
            raise ValueError('illegal None for both choices and get_choices')
        self.after_select = after_select
        self.result_formatter = result_formatter if result_formatter is not None else type(default)
        self.var = tk.StringVar(None, default)
        super().__init__(container, self.var, None)

        self.bind('<Button-1>', self.on_click)

    def get(self):
        try:
            return self.result_formatter(self.var.get())
        except ValueError:
            return None

    def on_click(self, _):
        """Refresh the choices in the list using the get_choices function"""
        self['menu'].delete(0, 'end')
        for choice in self.get_choices():
            self['menu'].add_command(label=choice, command=lambda c=choice: self.on_select(c))

    def on_select(self, choice):
        self.var.set(choice)
        if self.after_select is not None:
            self.after_select()
