"""Game logic and algorithm module"""
from random import randint
from dataclasses import dataclass
from typing import List, Callable
from abc import ABC, abstractmethod


@dataclass
class Turn:
    """Class to pass turn information around"""

    mode: bool  # what action to do with the number, true: take, false: split
    number: int  # value of number to operate with
    index: int | None = None  # index of number to operate with
    TAKE = True  # value for mode
    SPLIT = False  # value for mode


class Game:
    """Game logic class to seperate game from interface"""

    def __init__(self, length: int = 15):
        self.counts = [0] * 4
        self.numbers = []
        for _ in range(length):
            number = randint(0, len(self.counts) - 1)
            self.counts[number] += 1
            self.numbers.append(number)

        self.points = [0, 0]
        self.player = 0  # 0 is p1, 1 is p2
        self.done = False

    def copy(self):
        new = Game()
        new.counts = self.counts[:]
        new.numbers = self.numbers[:]
        new.points = self.points[:]
        new.player = self.player
        new.done = self.done
        return new

    def available_turns(self, include_index=False) -> List[Turn]:
        """Gets available turns for current game state"""

        turns: List[Turn] = []
        if self.done:
            return turns
        if not include_index:
            for number, amount in enumerate(self.counts):
                if amount > 0:
                    turns.append(Turn(Turn.TAKE, number))
                    if number % 2 == 1:
                        turns.append(Turn(Turn.SPLIT, number))
        else:
            for index, number in enumerate(self.numbers):
                turns.append(Turn(Turn.TAKE, number, index))
                if number % 2 == 1:
                    turns.append(Turn(Turn.SPLIT, number, index))
        return turns

    def do_turn(self, turn: Turn):  # Assumes the given turn is valid(from method above)
        """Does a turn which modifies game state"""
        if self.done:
            return

        self.counts[turn.number] -= 1
        if turn.index is None:
            self.numbers.remove(turn.number)
        else:
            self.numbers.pop(turn.index)

        if turn.mode == Turn.TAKE:
            self.points[self.player] += turn.number + 1
        else:
            new = turn.number // 2
            self.counts[new] += 2
            if turn.index is None:
                self.numbers.append(new)
                self.numbers.append(new)
            else:
                self.numbers.insert(turn.index, new)
                self.numbers.insert(turn.index, new)
            self.points[self.player] += turn.number // 2

        self.player = other_player_num(self.player)

        if sum(self.counts) <= 0:
            self.done = True


def other_player_num(number: int):
    return (number + 1) % 2


class Player(ABC):
    @abstractmethod
    def choose_turn(self, game: Game) -> Turn:
        ...


class MinMax(Player):
    def __init__(self, player_number: int, search_depth: int):
        self.number = player_number
        self.search_depth = search_depth

    def heuristic(self, game: Game) -> int:
        return game.points[self.number] - game.points[other_player_num(self.number)]

    def choose_turn(self, game: Game) -> Turn:
        best_estimate: int = -1_000_000
        best_turn: Turn

        for turn in game.available_turns(include_index=False):
            subgame = game.copy()
            subgame.do_turn(turn)
            if self.search_depth >= 1 and not subgame.done:
                other_player = MinMax(
                    other_player_num(self.number), self.search_depth - 1
                )
                other_turn = other_player.choose_turn(subgame)
                subgame.do_turn(other_turn)

            subgame_estimate = self.heuristic(subgame)
            if subgame_estimate > best_estimate:
                best_estimate = subgame_estimate
                best_turn = turn

        return best_turn
