"""Game logic and algorithm module"""
from random import randint
from dataclasses import dataclass
from typing import List


@dataclass
class Turn:
    """Class to pass turn information around"""

    number: int  # which number to operate with
    mode: bool  # what action to do with the number, true: take, false: split
    TAKE = True
    SPLIT = False


class Game:
    """Game logic class to seperate game from interface"""

    def __init__(self, length: int = 15):
        self.numbers = [0] * 4
        for _ in range(length):
            self.numbers[randint(0, len(self.numbers) - 1)] += 1
        self.points = [0, 0]
        self.player = 0  # 0 is p1, 1 is p2

    def __str__(self):
        return f"Punkti: {self.points}, Gājiens: {self.player+1}. spēlētājam"

    def available_turns(self) -> List[Turn]:
        """Gets available turns for current game state"""
        turns: List[Turn] = []
        for number, amount in enumerate(self.numbers):
            if amount > 0:
                turns.append(Turn(number, Turn.TAKE))
                if number % 2 == 1:
                    turns.append(Turn(number, Turn.SPLIT))
        return turns

    def do_turn(self, turn: Turn):  # Assumes the given turn is valid(from method above)
        """Does a turn which modifies game state"""
        self.numbers[turn.number] -= 1

        if turn.mode == Turn.TAKE:
            self.points[self.player] += turn.number + 1
        else:
            self.numbers[turn.number // 2] += 2
            self.points[self.player] += turn.number // 2

        self.player = (self.player + 1) % 2
