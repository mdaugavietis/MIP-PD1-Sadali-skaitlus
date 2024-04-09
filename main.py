"""Tk GUI module"""
import tkinter as tk
from functools import partial
from typing import List
import game
import startWindow


class GameGUI:

    def __init__(self, master, sequence_length=15):
        self.master = master
        self.master.configure(bg="#222831")
        self.game = game.Game(sequence_length)
        self.computer_players: List[game.Player | None] = [None, None]
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Sadali skaitļus")

        self.menuBar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.actionmenu = tk.Menu(self.menuBar, tearoff=0)

        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="Atjaunot", command=self.restart)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Iziet", command=exit)

        self.actionmenu = tk.Menu(self.menuBar, tearoff=0)
        self.actionmenu.add_command(label="Spēles veids")
        self.actionmenu.add_command(label="Ciparu skaits")

        self.actionmenu = tk.Menu(self.menuBar, tearoff=0)
        self.importsubgame = tk.Menu(self.actionmenu, tearoff=0)
        self.importsubnumber = tk.Menu(self.actionmenu, tearoff=0)
        self.importsubgame.add_command(
            label="MinMax pret cilvēku",
            command=partial(
                self.restart_with_computer,
                [game.MinMax(player_number=0, search_depth=4), None],
            ),
        )
        self.importsubgame.add_command(
            label="Cilvēks pret MinMax",
            command=partial(
                self.restart_with_computer,
                [None, game.MinMax(player_number=1, search_depth=4)],
            ),
        )

        self.importsubgame.add_command(
            label="AlphaBeta pret cilvēku",
            command=partial(
                self.restart_with_computer,
                [game.AlphaBeta(player_number=0, search_depth=4), None],
            ),
        )
        self.importsubgame.add_command(
            label="Cilvēks pret AlphaBeta",
            command=partial(
                self.restart_with_computer,
                [None, game.AlphaBeta(player_number=1, search_depth=4)],
            ),
        )

        for sequence_length in range(15, 21):
            self.importsubnumber.add_command(
                label=str(sequence_length),
                command=partial(self.restart_with_new_count, sequence_length),
            )

        self.actionmenu.add_cascade(menu=self.importsubgame, label="Spēles režīms")
        self.actionmenu.add_cascade(menu=self.importsubnumber,
                                    label="Ciparu skaits")

        self.menuBar.add_cascade(menu=self.filemenu, label="Spēlēt")
        self.menuBar.add_cascade(menu=self.actionmenu, label="Iestatījumi")

        self.master.config(menu=self.menuBar)

        self.info_label = tk.Label(self.master,
                                   text="",
                                   bg="#222831",
                                   fg="#eeeeee")
        self.info_label.pack()

        self.numbers_frame = tk.Frame(self.master, bg="#222831")
        self.numbers_frame.pack()

        self.mode_frame = tk.Frame(self.master, bg="#222831")
        self.mode_frame.pack()

        self.update_ui()

    def update_ui(self):
        info: str
        if not self.game.done:
            info = f"""Punkti:
                1. spēlētājs: {self.game.points[0]}
                2. spēlētājs: {self.game.points[1]}

                Gājiens: {self.game.player+1}. spēlētājam"""
        else:
            info = f"""Spēle beidzās ar rezultātu:
                1. spēlētājs: {self.game.points[0]}
                2. spēlētājs: {self.game.points[1]}

                """
        self.info_label.config(text=info)

        for widget in self.numbers_frame.winfo_children():
            widget.destroy()

        if self.computer_players[
                self.game.player] is not None and not self.game.done:
            computer_turn_button = tk.Button(
                self.numbers_frame,
                text="Izpildīt datora gājienu",
                command=partial(
                    self.turn,
                    self.computer_players[self.game.player].choose_turn(
                        self.game),
                ),
                bg="#00adb5",
                fg="#eeeeee",
            )
            computer_turn_button.pack()
        else:
            indexed_turns: List[List[game.Turn]] = [
                list() for _ in self.game.numbers
            ]
            for turn in self.game.available_turns(include_index=True):
                indexed_turns[turn.index].append(turn)

            for index, turns in enumerate(indexed_turns):
                number_button = tk.Button(
                    self.numbers_frame,
                    text=f"{turns[0].number + 1}",
                    command=partial(self.choose_mode, index, turns),
                    bg="#00adb5",
                    fg="#eeeeee",
                )
                number_button.grid(row=index // 8,
                                   column=index % 8,
                                   padx=5,
                                   pady=5)

    def choose_mode(self, selected_index: int, modes: List[game.Turn]):
        for index, button in enumerate(self.numbers_frame.winfo_children()):
            col: str
            if index == selected_index:
                col = "#2eeeee"
            else:
                col = "#00adb5"
            button.configure(bg=col)
        for widget in self.mode_frame.winfo_children():
            widget.destroy()

        for index, turn in enumerate(modes):
            label: str
            if turn.mode == game.Turn.TAKE:
                label = "Paņemt"
            else:
                label = "Sadalīt"

            button = tk.Button(
                self.mode_frame,
                text=label,
                command=partial(self.turn, turn),
                bg="#00adb5",
                fg="#eeeeee",
            )
            button.grid(row=0, column=index, padx=5, pady=5)

    def turn(self, turn: game.Turn):
        self.game.do_turn(turn)
        for widget in self.mode_frame.winfo_children():
            widget.destroy()
        self.update_ui()

    def restart_with_new_count(self, count):
        self.game = game.Game(count)
        self.update_ui()

    def restart(self):
        self.restart_with_new_count(len(self.game.numbers))

    def restart_with_computer(self,
                              computer_players: List[game.Player | None]):
        self.computer_players = computer_players
        self.restart()


def main(player1_mode, player2_mode, number_count):
    sequence_length = number_count
    root = tk.Tk()
    root.geometry("800x300")
    game_gui = GameGUI(root, sequence_length)

    computer_players = [None, None]
    if player1_mode != "Cilvēks":
        computer_players[0] = game.MinMax(player_number=0, search_depth=4)
        if player2_mode != "MinMax":
          computer_players[0] = game.AlphaBeta(player_number=1, search_depth=4)
    if player2_mode != "Cilvēks":
        computer_players[1] = game.MinMax(player_number=1, search_depth=4)
        if player2_mode != "MinMax":
          computer_players[1] = game.AlphaBeta(player_number=1, search_depth=4)

    game_gui.restart_with_computer(computer_players)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    main()
    root.mainloop()
