from random import randint


class Game:
    def __init__(self, length: int):
        self.points = [0, 0]
        length = max(min(length, 20), 15)
        self.numbers = [randint(1, 4) for i in range(length)]
        self.player = 0  # 0 is p1, 1 is p2

    def __str__(self):
        return f"""
Punkti: {self.points}, Gājiens: {self.player+1}. spēlētājam
Skaitļi (indekss, skaitlis): {list(enumerate(self.numbers))}
        """

    def turn(self, mode: bool, ind: int):
        # False is take, True is split
        if mode:
            self.points[self.player] += self.numbers[ind]
            self.numbers.pop(ind)
        else:
            if self.numbers[ind] % 2 == 1:
                print("nevar sadalīt")
            else:
                self.numbers[ind] //= 2
                self.numbers.insert(ind, self.numbers[ind])
                self.points[self.player] += self.numbers[ind] // 2
        self.player = (self.player + 1) % 2


def main():
    sequence_length = int(input("Ievadi cik skaitļus ģenerēt: "))
    game = Game(sequence_length)

    while len(game.numbers) > 0:
        print(game)
        command = input("(P)aņem vai (S)adali skaitli indeksā: ")

        mode = command[0].lower()
        ind = int(command[1:])
        game.turn(mode == "p", ind)

    print(f"Spēle beidzās ar rezultātu {game.points}")

if __name__ == "__main__":
    main()
