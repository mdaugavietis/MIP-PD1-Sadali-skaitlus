"""Tk GUI module"""
import tkinter as tk
from functools import partial
import game


class GameGUI:
    def __init__(self, master, sequence_length=15):
        self.master = master
        self.master.configure(bg="#222831")
        self.game = game.Game(sequence_length)
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Sadali skaitļus")

        self.menuBar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.actionmenu = tk.Menu(self.menuBar, tearoff=0)

        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="Restart", command=self.restart)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=exit)

        self.actionmenu = tk.Menu(self.menuBar, tearoff=0)
        self.actionmenu.add_command(label="Game mode")
        self.actionmenu.add_command(label="Number count")

        self.actionmenu = tk.Menu(self.menuBar, tearoff=0)
        self.importsubgame = tk.Menu(self.actionmenu, tearoff=0)
        self.importsubnumber = tk.Menu(self.actionmenu, tearoff=0)
        self.importsubgame.add_command(label="player VS player")
        self.importsubgame.add_command(label="player VS computer")

        for sequence_length in range(15, 21):
            self.importsubnumber.add_command(
                label=str(sequence_length),
                command=partial(self.restart_with_new_count, sequence_length),
            )

        self.actionmenu.add_cascade(menu=self.importsubgame, label="Game mode")
        self.actionmenu.add_cascade(menu=self.importsubnumber, label="Number count")

        self.menuBar.add_cascade(menu=self.filemenu, label="Game")
        self.menuBar.add_cascade(menu=self.actionmenu, label="Options")

        self.master.config(menu=self.menuBar)

        self.info_label = tk.Label(self.master, text="", bg="#222831", fg="#eeeeee")
        self.info_label.pack()

        self.numbers_frame = tk.Frame(self.master, bg="#222831")
        self.numbers_frame.pack()

        self.update_ui()

    def update_ui(self):
        self.info_label.config(text=str(self.game))

        for widget in self.numbers_frame.winfo_children():
            widget.destroy()

        turns = self.game.available_turns()
        for number, amount in enumerate(self.game.numbers):
            amount_label = tk.Label(
                self.numbers_frame,
                text=f'Daudzums: {amount}',
                bg="#393e46",
                fg="#eeeeee",
            )
            amount_label.grid(row=0, column=number, padx=5, pady=5)

            number_label = tk.Label(
                self.numbers_frame,
                text=f"Skaitlis: {number+1}",
                bg="#393e46",
                fg="#eeeeee",
            )
            number_label.grid(row=1, column=number, padx=5, pady=5)

            turn = game.Turn(number, game.Turn.TAKE)
            number_take = tk.Button(
                self.numbers_frame,
                text="Paņemt",
                command=partial(self.turn, turn),
                bg="#00adb5",
                fg="#eeeeee",
            )
            if turn not in turns:
                number_take.configure(state="disabled")
            number_take.grid(row=2, column=number, padx=5, pady=5)

            if number % 2 == 1:
                turn = game.Turn(number, game.Turn.SPLIT)
                number_split = tk.Button(
                    self.numbers_frame,
                    text="Sadalīt",
                    command=partial(self.turn, turn),
                    bg="#00adb5",
                    fg="#eeeeee",
                )
                if turn not in turns:
                    number_split.configure(state="disabled")
                number_split.grid(row=3, column=number, padx=5, pady=5)

        if sum(self.game.numbers) <= 0:
            self.display_result()

    def display_result(self):
        result_label = tk.Label(
            self.master,
            text=f"Spēle beidzās ar rezultātu {self.game.points}",
            bg="#222831",
            fg="#eeeeee",
        )
        result_label.pack()

    def turn(self, turn: game.Turn):
        self.game.do_turn(turn)
        self.update_ui()

    def restart(self):
        self.restart_with_new_count(len(self.game.numbers))

    def restart_with_new_count(self, count):
        self.game = game.Game(count)
        self.update_ui()


def main():
    root = tk.Tk()
    root.geometry("600x140")
    sequence_length = 15
    GameGUI(root, sequence_length)
    root.mainloop()


if __name__ == "__main__":
    main()
