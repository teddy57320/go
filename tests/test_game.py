import unittest
import numpy as np
from src.game import Game
from src.utils import Stone
from tests.utils import (
    capture1, capture2, capture3,
    self_destruct1, self_destruct2, self_destruct3)

class TestBoard(unittest.TestCase):
    '''
    Test case for placement of stones on the board
    '''
    def setUp(self):
        self.black_stone = 'b'
        self.white_Stone = 'w'
        self.board_size = 7

        configs = {'black_stone': self.black_stone,
                   'white_stone': self.white_Stone,
                   'board_size': self.board_size,
                   'enable_self_destruct': True
        }

        self.game = Game(configs)

    def test__place_stone(self):
        self.game.place_black(4, 4)
        self.game.place_white(4, 5)
        self.assertEqual(self.game.board[4, 4], Stone.BLACK)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(np.where(self.game.board == Stone.BLACK), (4, 4))
        self.assertEqual(np.where(self.game.board == Stone.WHITE), (4, 5))

    def test__capture1(self):
        capture1(self.game)
        self.assertEqual(self.game.board[4, 4], Stone.EMPTY)
        self.assertEqual(self.game.board[4, 3], Stone.WHITE)
        self.assertEqual(self.game.board[3, 4], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(self.game.num_black_captured, 1)

    def test__capture2(self):
        capture2(self.game)
        self.assertFalse(np.any(self.game.board == Stone.BLACK))
        self.assertEqual(self.game.board[2, 4], Stone.WHITE)
        self.assertEqual(self.game.board[3, 3], Stone.WHITE)
        self.assertEqual(self.game.board[4, 2], Stone.WHITE)
        self.assertEqual(self.game.board[5, 3], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(self.game.board[3, 5], Stone.WHITE)
        self.assertEqual(self.game.num_black_captured, 3)

    def test__capture3(self):
        capture3(self.game)
        self.assertFalse(np.any(self.game.board == Stone.BLACK))
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(self.game.board[4, 3], Stone.WHITE)
        self.assertEqual(self.game.board[3, 4], Stone.WHITE)
        self.assertEqual(self.game.board[3, 3], Stone.WHITE)
        self.assertEqual(self.game.board[5, 5], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.num_black_captured, 1)

    def test__self_destruct1(self):
        self_destruct1(self.game)
        self.assertEqual(self.game.board[4, 4], Stone.EMPTY)
        self.assertEqual(self.game.board[4, 3], Stone.WHITE)
        self.assertEqual(self.game.board[3, 4], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(self.game.num_black_captured, 1)

    def test__self_destruct2(self):
        self_destruct2(self.game)
        self.assertFalse(np.any(self.game.board == Stone.BLACK))
        self.assertEqual(self.game.board[2, 4], Stone.WHITE)
        self.assertEqual(self.game.board[3, 3], Stone.WHITE)
        self.assertEqual(self.game.board[4, 2], Stone.WHITE)
        self.assertEqual(self.game.board[5, 3], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(self.game.board[3, 5], Stone.WHITE)
        self.assertEqual(self.game.num_black_captured, 3)

    def test__self_destruct3(self):
        self_destruct3(self.game)

        for y, x in [(2, 2), (2, 3), (2, 4), (3, 4), (3, 3), (4, 4), (4, 3), (4, 2), (3, 2)]:
            self.assertEqual(self.game.board[y, x], Stone.EMPTY)

        for y, x in [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                     (2, 5), (3, 5), (4, 5), (5, 5),
                     (5, 4), (5, 3), (5, 2), (5, 1),
                     (4, 1), (3, 1), (2, 1)]:
            self.assertEqual(self.game.board[y, x], Stone.WHITE)
        self.assertEqual(self.game.num_black_captured, 9)


class TestScore(unittest.TestCase):
    '''
    Test case for score tallying
    '''
    def setUp(self):
        self.black_stone = 'b'
        self.white_Stone = 'w'
        self.board_size = 7

        configs = {'black_stone': self.black_stone,
                   'white_stone': self.white_Stone,
                   'board_size': self.board_size,
                   'enable_self_destruct': False
        }

        self.game = Game(configs)

    def test__capture1(self):
        capture1(self.game)
        scores = self.game.get_scores()
        self.assertEqual(scores[Stone.BLACK], -1)
        self.assertEqual(scores[Stone.WHITE], 45)

    def test__capture2(self):
        capture2(self.game)
        scores = self.game.get_scores()
        self.assertEqual(scores[Stone.BLACK], -3)
        self.assertEqual(scores[Stone.WHITE], 42)

    def test__capture3(self):
        capture3(self.game)
        scores = self.game.get_scores()
        self.assertEqual(scores[Stone.BLACK], -1)
        self.assertEqual(scores[Stone.WHITE], 43)

    def test__neutral(self):
        capture2(self.game)
        self.game.place_black(1, 1)
        scores = self.game.get_scores()
        self.assertEqual(scores[Stone.BLACK], -3)
        self.assertEqual(scores[Stone.WHITE], 3)
