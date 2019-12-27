import unittest
import numpy as np
from src.game import Game, Group
from src.utils import Stone

def capture_simple(game):
    game.place_black(4, 4)
    game.place_white(4, 5)
    game.place_white(4, 3)
    game.place_white(3, 4)
    game.place_white(5, 4)

def capture_complex(game):
    for y, x in [(4, 3), (3, 4), (4, 4)]:
        game.place_black(y, x)
    for y, x in [(2, 4), (3, 3), (4, 2), (5, 3), (5, 4), (4, 5), (3, 5)]:
        game.place_white(y, x)

def self_destruct_simple(game):
    game.place_white(4, 5)
    game.place_white(4, 3)
    game.place_white(3, 4)
    game.place_white(5, 4)
    game.place_black(4, 4)


class TestGame(unittest.TestCase):

    def setUp(self):
        self.black_stone = 'b'
        self.white_Stone = 'w'
        self.board_size = 7

        configs = {'black_stone': self.black_stone,
                   'white_stone': self.white_Stone,
                   'board_size': self.board_size
        }

        self.game = Game(configs)

    def test__place_stone(self):
        self.game.place_black(4, 4)
        self.game.place_white(4, 5)
        self.assertEqual(self.game.board[4, 4], Stone.BLACK)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(np.where(self.game.board == Stone.BLACK), (4, 4))
        self.assertEqual(np.where(self.game.board == Stone.WHITE), (4, 5))

    def test__capture_simple(self):
        capture_simple(self.game)
        self.assertEqual(self.game.board[4, 4], Stone.EMPTY)
        self.assertEqual(self.game.board[4, 3], Stone.WHITE)
        self.assertEqual(self.game.board[3, 4], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)

    def test__capture_complex(self):
        capture_complex(self.game)
        self.assertFalse(np.any(self.game.board == Stone.BLACK))
        self.assertEqual(self.game.board[2, 4], Stone.WHITE)
        self.assertEqual(self.game.board[3, 3], Stone.WHITE)
        self.assertEqual(self.game.board[4, 2], Stone.WHITE)
        self.assertEqual(self.game.board[5, 3], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(self.game.board[3, 5], Stone.WHITE)

    def test__self_destruct_simple(self):
        self_destruct_simple(self.game)
        self.assertEqual(self.game.board[4, 4], Stone.EMPTY)
        self.assertEqual(self.game.board[4, 3], Stone.WHITE)
        self.assertEqual(self.game.board[3, 4], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)


class TestGameGroups(unittest.TestCase):

    def setUp(self):
        self.black_stone = 'b'
        self.white_Stone = 'w'
        self.board_size = 7

        configs = {'black_stone': self.black_stone,
                   'white_stone': self.white_Stone,
                   'board_size': self.board_size
        }

        self.game = Game(configs)

    def test__place_stone(self):
        self.game.place_black(3, 3)
        group = self.game.gm._get_group(3, 3)
        self.assertEqual(type(group), Group)
        self.assertEqual(self.game.board[3, 3], Stone.BLACK)
        self.assertEqual(group.stone, Stone.BLACK)

    def test__liberties_basic(self):

        # centre of board - 4 liberties
        self.game.place_black(3, 3)
        group = self.game.gm._get_group(3, 3)
        self.assertIn((3, 2), group.liberties)
        self.assertIn((3, 4), group.liberties)
        self.assertIn((2, 3), group.liberties)
        self.assertIn((4, 3), group.liberties)
        self.assertEqual(len(group.liberties), 4)
        self.assertEqual(len(group.removed_liberties), 0)

        # side of board - 3 liberties
        self.game.place_white(3, 0)
        group = self.game.gm._get_group(3, 0)
        self.assertIn((4, 0), group.liberties)
        self.assertIn((2, 0), group.liberties)
        self.assertIn((3, 1), group.liberties)
        self.assertEqual(len(group.liberties), 3)
        self.assertEqual(len(group.removed_liberties), 0)

        # corner of board - 2 liberties
        self.game.place_black(0, 0)
        group = self.game.gm._get_group(0, 0)
        self.assertIn((0, 1), group.liberties)
        self.assertIn((1, 0), group.liberties)
        self.assertEqual(len(group.liberties), 2)
        self.assertEqual(len(group.removed_liberties), 0)

    def test__merge(self):

        # place adjacent black stones and have the two groups merge into the same one
        self.game.place_black(4, 1)
        self.game.place_black(4, 2)
        self.assertEqual(self.game.gm._get_group(4, 1), self.game.gm._get_group(4, 2))
        black_group = self.game.gm._get_group(4, 1)
        self.assertIn((3, 1), black_group.liberties)
        self.assertIn((3, 2), black_group.liberties)
        self.assertIn((5, 1), black_group.liberties)
        self.assertIn((5, 2), black_group.liberties)
        self.assertIn((4, 0), black_group.liberties)
        self.assertIn((4, 3), black_group.liberties)
        self.assertEqual(len(black_group.liberties), 6)
        self.assertEqual(len(black_group.removed_liberties), 0)

        # place an adjacent, opposite colour stone does not merge
        # black group has its liberties decremented
        self.game.place_white(4, 3)
        self.assertEqual(self.game.gm._get_group(4, 1), self.game.gm._get_group(4, 2))
        black_group = self.game.gm._get_group(4, 1)
        self.assertIn((3, 1), black_group.liberties)
        self.assertIn((3, 2), black_group.liberties)
        self.assertIn((5, 1), black_group.liberties)
        self.assertIn((5, 2), black_group.liberties)
        self.assertIn((4, 0), black_group.liberties)
        self.assertEqual(len(black_group.liberties), 5)
        self.assertIn((4, 3), black_group.removed_liberties)
        self.assertEqual(len(black_group.removed_liberties), 1)

        # new white group has only 3 liberties
        white_group = self.game.gm._get_group(4, 3)
        self.assertIn((4, 4), white_group.liberties)
        self.assertIn((3, 3), white_group.liberties)
        self.assertIn((5, 3), white_group.liberties)
        self.assertEqual(len(white_group.liberties), 3)
        self.assertIn((4, 2), white_group.removed_liberties)
        self.assertEqual(len(white_group.removed_liberties), 1)

    def test__capture_simple(self):
        capture_simple(self.game)

        black_group = self.game.gm._get_group(4, 4)
        self.assertIsNone(black_group)

        self.assertNotEqual(self.game.gm._get_group(4, 5), self.game.gm._get_group(4, 3))
        self.assertNotEqual(self.game.gm._get_group(4, 5), self.game.gm._get_group(3, 4))
        self.assertNotEqual(self.game.gm._get_group(4, 5), self.game.gm._get_group(5, 4))
        self.assertNotEqual(self.game.gm._get_group(4, 3), self.game.gm._get_group(3, 4))
        self.assertNotEqual(self.game.gm._get_group(4, 3), self.game.gm._get_group(5, 4))
        self.assertNotEqual(self.game.gm._get_group(3, 4), self.game.gm._get_group(5, 4))

        white_group1 = self.game.gm._get_group(4, 5)
        self.assertIn((4, 6), white_group1.liberties)
        self.assertIn((4, 4), white_group1.liberties)
        self.assertIn((3, 5), white_group1.liberties)
        self.assertIn((5, 5), white_group1.liberties)
        self.assertEqual(len(white_group1.liberties), 4)

        white_group2 = self.game.gm._get_group(4, 3)
        self.assertIn((4, 4), white_group2.liberties)
        self.assertIn((4, 2), white_group2.liberties)
        self.assertIn((3, 3), white_group2.liberties)
        self.assertIn((5, 3), white_group2.liberties)
        self.assertEqual(len(white_group2.liberties), 4)

        white_group3 = self.game.gm._get_group(3, 4)
        self.assertIn((3, 5), white_group3.liberties)
        self.assertIn((3, 3), white_group3.liberties)
        self.assertIn((2, 4), white_group3.liberties)
        self.assertIn((4, 4), white_group3.liberties)
        self.assertEqual(len(white_group3.liberties), 4)

        white_group4 = self.game.gm._get_group(5, 4)
        self.assertIn((5, 5), white_group4.liberties)
        self.assertIn((5, 3), white_group4.liberties)
        self.assertIn((4, 4), white_group4.liberties)
        self.assertIn((6, 4), white_group4.liberties)
        self.assertEqual(len(white_group4.liberties), 4)

    def test__self_destruct_simple(self):
        self_destruct_simple(self.game)

        black_group = self.game.gm._get_group(4, 4)
        self.assertIsNone(black_group)

        self.assertNotEqual(self.game.gm._get_group(4, 5), self.game.gm._get_group(4, 3))
        self.assertNotEqual(self.game.gm._get_group(4, 5), self.game.gm._get_group(3, 4))
        self.assertNotEqual(self.game.gm._get_group(4, 5), self.game.gm._get_group(5, 4))
        self.assertNotEqual(self.game.gm._get_group(4, 3), self.game.gm._get_group(3, 4))
        self.assertNotEqual(self.game.gm._get_group(4, 3), self.game.gm._get_group(5, 4))
        self.assertNotEqual(self.game.gm._get_group(3, 4), self.game.gm._get_group(5, 4))

        white_group1 = self.game.gm._get_group(4, 5)
        self.assertIn((4, 6), white_group1.liberties)
        self.assertIn((4, 4), white_group1.liberties)
        self.assertIn((3, 5), white_group1.liberties)
        self.assertIn((5, 5), white_group1.liberties)
        self.assertEqual(len(white_group1.liberties), 4)

        white_group2 = self.game.gm._get_group(4, 3)
        self.assertIn((4, 4), white_group2.liberties)
        self.assertIn((4, 2), white_group2.liberties)
        self.assertIn((3, 3), white_group2.liberties)
        self.assertIn((5, 3), white_group2.liberties)
        self.assertEqual(len(white_group2.liberties), 4)

        white_group3 = self.game.gm._get_group(3, 4)
        self.assertIn((3, 5), white_group3.liberties)
        self.assertIn((3, 3), white_group3.liberties)
        self.assertIn((2, 4), white_group3.liberties)
        self.assertIn((4, 4), white_group3.liberties)
        self.assertEqual(len(white_group3.liberties), 4)

        white_group4 = self.game.gm._get_group(5, 4)
        self.assertIn((5, 5), white_group4.liberties)
        self.assertIn((5, 3), white_group4.liberties)
        self.assertIn((4, 4), white_group4.liberties)
        self.assertIn((6, 4), white_group4.liberties)
        self.assertEqual(len(white_group4.liberties), 4)
