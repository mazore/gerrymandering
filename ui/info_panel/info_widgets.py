import tkinter as tk


class PeopleCountInfo(tk.Frame):
    def __init__(self, info_panel):
        self.root = info_panel.root
        super().__init__(info_panel)

        tk.Label(self, font='Consolas 9', text='people: ').pack(side='left')
        self.blue_var = tk.StringVar()
        tk.Label(self, fg='#5868aa', font='Consolas 9', textvariable=self.blue_var).pack(side='left')
        tk.Label(self, font='Consolas 9', text='-').pack(side='left')
        self.red_var = tk.StringVar()
        tk.Label(self, fg='#f95955', font='Consolas 9', textvariable=self.red_var).pack(side='left')

        self.update_info()

    def update_info(self):
        score = dict(blue=0, red=0)
        for row in self.root.canvas.people_grid:
            for person in row:
                score[person.party.name] += 1
        self.blue_var.set(score['blue'])
        self.red_var.set(score['red'])


class ScoreInfo(tk.Frame):
    def __init__(self, info_panel):
        self.root = info_panel.root
        super().__init__(info_panel)

        self.blue_var = tk.StringVar()
        tk.Label(self, fg='#5868aa', font='Consolas 15', textvariable=self.blue_var).pack(side='left')
        tk.Label(self, font='Consolas 15', text='-').pack(side='left')
        self.red_var = tk.StringVar()
        tk.Label(self, fg='#f95955', font='Consolas 15', textvariable=self.red_var).pack(side='left')
        tk.Label(self, font='Consolas 15', text='-').pack(side='left')
        self.tie_var = tk.StringVar(value='0')
        tk.Label(self, fg='gray', font='Consolas 15', textvariable=self.tie_var).pack(side='left')

        self.update_info()

    def update_info(self):
        score = self.root.canvas.get_score()
        self.blue_var.set(score['blue'])
        self.red_var.set(score['red'])
        self.tie_var.set(score['tie'])


class SwapsDoneInfo(tk.Label):
    def __init__(self, info_panel):
        self.root = info_panel.root
        self.var = tk.StringVar()
        self.update_info()
        super().__init__(info_panel, font='Consolas 9', textvariable=self.var)

    def update_info(self):
        self.var.set(f'swaps_done: {self.root.canvas.swap_manager.swaps_done}')
