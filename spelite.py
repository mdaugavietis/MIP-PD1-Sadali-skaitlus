import tkinter as tk
from random import randint


class Game:
    def __init__(self, length: int):
        self.points = [0, 0]
        length = max(min(length, 20), 15)
        self.numbers = [randint(1, 4) for _ in range(length)]
        self.player = 0  # 0 is p1, 1 is p2
        
    def reset(self, length: int):
        self.points = [0, 0]
        length = max(min(length, 20), 15)
        self.numbers = [randint(1, 4) for _ in range(length)]
        self.player = 0 

    def turn(self, mode: bool, ind: int):
        # False is take, True is split
        if mode:
            self.points[self.player] += self.numbers[ind]
            self.numbers.pop(ind)
            self.player = (self.player + 1) % 2
        else:
            if self.numbers[ind] % 2 == 1:
                print("Nevar sadalīt")
            else:
                self.numbers[ind] //= 2
                self.numbers.insert(ind, self.numbers[ind])
                self.points[self.player] += self.numbers[ind] // 2
                self.player = (self.player + 1) % 2


class GameGUI:
    def __init__(self, master, sequence_length):
        self.master = master
        self.master.configure(bg="#222831")
        self.game = Game(sequence_length)
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Spēle")
        
        self.menuBar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.actionmenu = tk.Menu(self.menuBar, tearoff=0)
        
        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="Restart", command=self.restart_game)
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
        self.importsubnumber.add_command(label="15", command=lambda: self.submit_number_count(15))
        self.importsubnumber.add_command(label="16", command=lambda: self.submit_number_count(16))
        self.importsubnumber.add_command(label="17", command=lambda: self.submit_number_count(17))
        self.importsubnumber.add_command(label="18", command=lambda: self.submit_number_count(18))
        self.importsubnumber.add_command(label="19", command=lambda: self.submit_number_count(19))
        self.importsubnumber.add_command(label="20", command=lambda: self.submit_number_count(20))
        self.actionmenu.add_cascade(menu=self.importsubgame, label="Game mode")
        self.actionmenu.add_cascade(menu=self.importsubnumber,label="Number count")

        
        self.menuBar.add_cascade(menu=self.filemenu, label="Game")
        self.menuBar.add_cascade(menu=self.actionmenu, label="Options")
        
        self.master.config(menu=self.menuBar)

        self.info_label = tk.Label(self.master, text="", bg="#222831", fg="#eeeeee")
        self.info_label.pack()

        self.numbers_frame = tk.Frame(self.master, bg="#222831")
        self.numbers_frame.pack()

        self.command_entry = tk.Entry(self.master, bg="#30475e", fg="#eeeeee")
        self.command_entry.pack()

        buttonFrame = tk.Frame(self.master, bg="#222831")
        buttonFrame.pack(fill='x')

        self.split_button = tk.Button(buttonFrame, text="Sadalīt", command=lambda: self.submit_command("split"),
                                      bg="#00adb5", fg="#eeeeee") 
        self.split_button.pack(side=tk.RIGHT)

        self.take_button = tk.Button(buttonFrame, text="Paņemt", command=lambda: self.submit_command("take"),
                                     bg="#00adb5", fg="#eeeeee")
        self.take_button.pack(side=tk.LEFT)

        self.update_ui()

    def update_ui(self):
        self.info_label.config(text=f"Punkti: {self.game.points}, Gājiens: {self.game.player + 1}. spēlētājam")

        for widget in self.numbers_frame.winfo_children():
            widget.destroy()

        for index, number in enumerate(self.game.numbers):
            number_button = tk.Button(self.numbers_frame, text=str(number),
                                      command=lambda i=index: self.turn(i), bg="#393e46", fg="#eeeeee")
            number_button.grid(row=0, column=index, padx=5, pady=5)

        if len(self.game.numbers) == 0:
            self.display_result()

    def display_result(self):
        result_label = tk.Label(self.master, text=f"Spēle beidzās ar rezultātu {self.game.points}",
                                bg="#222831", fg="#eeeeee")  
        result_label.pack()

    def turn(self, index):
        self.command_entry.delete(0, tk.END)
        self.command_entry.insert(tk.END, f"P{index}")

    def submit_command(self, action):
        command = self.command_entry.get().strip()
        if command:
            ind = int(command[1:])
            if action == "take":
                self.game.turn(True, ind)
            elif action == "split":
                self.game.turn(False, ind)
            self.update_ui()
            self.command_entry.delete(0, tk.END)
            
    def restart_game(self):
        sequence_length = len(self.game.numbers) 
        self.game.reset(sequence_length)
        self.update_ui()
        
    def submit_number_count(self, count):
        self.game.reset(count)
        self.update_ui()


def main():
    root = tk.Tk()
    root.geometry("600x140")
    sequence_length = 15
    game_gui = GameGUI(root, sequence_length)
    root.mainloop()


if __name__ == "__main__":
    main()
