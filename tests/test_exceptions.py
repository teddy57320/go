import unittest
from src.game import Game
from src.utils import Stone
from src.exceptions import SelfDestructException, KoException

from tests.utils import (
    self_destruct1, self_destruct2, self_destruct3)

class TestSelfDestructDisabled(unittest.TestCase):
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
        
    def test__self_destruct1(self):
        with self.assertRaises(SelfDestructException):
            self_destruct1(self.game)
        self.assertEqual(self.game.board[4, 4], Stone.EMPTY)
        self.assertEqual(self.game.board[4, 3], Stone.WHITE)
        self.assertEqual(self.game.board[3, 4], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(self.game.num_black_captured, 0)
        self.assertIsNone(self.game.gm._get_group(4, 4))
        
        self.assertFalse(self.game.gm.is_same_group(4, 5, 4, 3))
        self.assertFalse(self.game.gm.is_same_group(4, 5, 3, 4))
        self.assertFalse(self.game.gm.is_same_group(4, 5, 5, 4))
        self.assertFalse(self.game.gm.is_same_group(4, 3, 3, 4))
        self.assertFalse(self.game.gm.is_same_group(4, 3, 5, 4))
        self.assertFalse(self.game.gm.is_same_group(3, 4, 5, 4))

    def test__self_destruct2(self):
        with self.assertRaises(SelfDestructException):
            self_destruct2(self.game)
        
        self.assertEqual(self.game.board[4, 3], Stone.BLACK)
        self.assertEqual(self.game.board[3, 4], Stone.BLACK)
        self.assertEqual(self.game.board[2, 4], Stone.WHITE)
        self.assertEqual(self.game.board[3, 3], Stone.WHITE)
        self.assertEqual(self.game.board[4, 2], Stone.WHITE)
        self.assertEqual(self.game.board[5, 3], Stone.WHITE)
        self.assertEqual(self.game.board[5, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 5], Stone.WHITE)
        self.assertEqual(self.game.board[3, 5], Stone.WHITE)
        self.assertEqual(self.game.num_black_captured, 0)

        self.assertTrue(self.game.gm.is_same_group(5, 3, 5, 4))
        self.assertTrue(self.game.gm.is_same_group(4, 5, 3, 5))
        
        self.assertFalse(self.game.gm.is_same_group(2, 4, 3, 3))
        self.assertFalse(self.game.gm.is_same_group(2, 4, 4, 2))
        self.assertFalse(self.game.gm.is_same_group(2, 4, 5, 3))
        self.assertFalse(self.game.gm.is_same_group(2, 4, 4, 5))
        self.assertFalse(self.game.gm.is_same_group(3, 3, 4, 2))
        self.assertFalse(self.game.gm.is_same_group(3, 3, 5, 3))
        self.assertFalse(self.game.gm.is_same_group(3, 3, 4, 5))
        self.assertFalse(self.game.gm.is_same_group(4, 2, 5, 3))
        self.assertFalse(self.game.gm.is_same_group(4, 2, 4, 5))
        self.assertFalse(self.game.gm.is_same_group(5, 3, 4, 5))

        white_group1 = self.game.gm._get_group(2, 4)
        self.assertTrue(white_group1.has_liberty((2, 3)))
        self.assertTrue(white_group1.has_liberty((2, 5)))
        self.assertTrue(white_group1.has_liberty((1, 4)))

        white_group2 = self.game.gm._get_group(3, 3)
        self.assertTrue(white_group2.has_liberty((3, 2)))
        self.assertTrue(white_group2.has_liberty((2, 3)))

        white_group3 = self.game.gm._get_group(4, 2)
        self.assertTrue(white_group3.has_liberty((3, 2)))
        self.assertTrue(white_group3.has_liberty((5, 2)))
        self.assertTrue(white_group3.has_liberty((4, 1)))

        white_group4 = self.game.gm._get_group(5, 3)
        self.assertTrue(white_group4.has_liberty((5, 2)))
        self.assertTrue(white_group4.has_liberty((5, 5)))
        self.assertTrue(white_group4.has_liberty((4, 4)))
        self.assertTrue(white_group4.has_liberty((6, 3)))
        self.assertTrue(white_group4.has_liberty((6, 4)))

        white_group5 = self.game.gm._get_group(3, 5)
        self.assertTrue(white_group5.has_liberty((3, 6)))
        self.assertTrue(white_group5.has_liberty((4, 4)))
        self.assertTrue(white_group5.has_liberty((4, 6)))
        self.assertTrue(white_group5.has_liberty((2, 5)))
        self.assertTrue(white_group5.has_liberty((5, 5)))

    def test__self_destruct3(self):
        with self.assertRaises(SelfDestructException):
            self_destruct3(self.game)

        for y, x in [(2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (3, 2)]:
            self.assertEqual(self.game.board[y, x], Stone.BLACK)

        for y, x in [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                     (2, 5), (3, 5), (4, 5), (5, 5),
                     (5, 4), (5, 3), (5, 2), (5, 1),
                     (4, 1), (3, 1), (2, 1)]:
            self.assertEqual(self.game.board[y, x], Stone.WHITE)
        self.assertEqual(self.game.num_black_captured, 0)


class TestKo(unittest.TestCase):
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

    def test__ko1(self):
        self.game.place_black(2, 2)
        self.game.place_black(3, 1)
        self.game.place_black(4, 2)
        self.game.place_white(2, 3)
        self.game.place_white(3, 4)
        self.game.place_white(4, 3)
        self.game.place_black(3, 3)
        self.game.place_white(3, 2)

        with self.assertRaises(KoException):
            self.game.place_black(3, 3)

        self.assertEqual(self.game.board[3, 3], Stone.EMPTY)
        self.assertEqual(self.game.board[2, 2], Stone.BLACK)
        self.assertEqual(self.game.board[3, 1], Stone.BLACK)
        self.assertEqual(self.game.board[4, 2], Stone.BLACK)
        self.assertEqual(self.game.board[2, 3], Stone.WHITE)
        self.assertEqual(self.game.board[3, 4], Stone.WHITE)
        self.assertEqual(self.game.board[4, 3], Stone.WHITE)
        self.assertEqual(self.game.board[3, 2], Stone.WHITE)

    def test_ko2(self):
        self.game.place_black(0, 0)
        self.game.place_black(1, 1)
        self.game.place_black(0, 2)
        self.game.place_white(1, 0)
        self.game.place_white(0, 1)

        with self.assertRaises(KoException):
            self.game.place_black(0, 0)
        
        self.assertEqual(self.game.board[0, 0], Stone.EMPTY)
        self.assertEqual(self.game.board[1, 1], Stone.BLACK)
        self.assertEqual(self.game.board[0, 2], Stone.BLACK)
        self.assertEqual(self.game.board[1, 0], Stone.WHITE)
        self.assertEqual(self.game.board[0, 1], Stone.WHITE)