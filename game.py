"""Game logic and algorithm module"""
from random import randint
from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod
from typing import Tuple



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

    def do_turn(
            self,
            turn: Turn):  # Assumes the given turn is valid(from method above)
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


class GameNode:

    def __init__(self, game: Game, turn: Turn | None, depth: int):
        self.estimate = 0
        self.game = game
        self.turn = turn
        self.children = []
        if depth > 0:
            for new_turn in self.game.available_turns():
                tmp_game = game.copy()
                tmp_game.do_turn(new_turn)
                self.children.append(GameNode(tmp_game, new_turn, depth - 1))

    def do_estimate(self, maximize: bool):
        if len(self.children) == 0:
            self.estimate = self.game.points[0] - self.game.points[1]
            return

        if maximize:
            self.estimate = -1000
        else:
            self.estimate = 1000

        for state in self.children:
            state.do_estimate(not maximize)
            if maximize:
                self.estimate = max(self.estimate, state.estimate)
            else:
                self.estimate = min(self.estimate, state.estimate)


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

    def choose_turn(self, game: Game) -> Turn:
        root = GameNode(game.copy(), None, self.search_depth)

        root.do_estimate(self.number == 0)

        best_turn: Turn
        for state in root.children:
            if state.estimate == root.estimate:
                best_turn = state.turn

        return best_turn

class AlphaBeta(Player):
  def __init__(self, player_number: int, search_depth: int):
      self.number = player_number
      self.search_depth = search_depth

  def choose_turn(self, game: Game) -> Turn:
      root = GameNode(game.copy(), None, self.search_depth)
      _, best_turn = self.minimax(root, -float('inf'), float('inf'), self.number == 0)
      return best_turn

  def minimax(self, node: GameNode, alpha: float, beta: float, maximize: bool) -> Tuple[float, Turn]:
      if len(node.children) == 0:
          return self.evaluate(node), node.turn

      if maximize:
          value = -float('inf')
          best_turn = None
          for state in node.children:
              child_value, _ = self.minimax(state, alpha, beta, False)
              if child_value > value:
                  value = child_value
                  best_turn = state.turn
              alpha = max(alpha, value)
              if beta <= alpha:
                  break
          return value, best_turn
      else:
          value = float('inf')
          best_turn = None
          for state in node.children:
              child_value, _ = self.minimax(state, alpha, beta, True)
              if child_value < value:
                  value = child_value
                  best_turn = state.turn
              beta = min(beta, value)
              if beta <= alpha:
                  break
          return value, best_turn

  def evaluate(self, node: GameNode) -> float:
      return node.game.points[0] - node.game.points[1]
