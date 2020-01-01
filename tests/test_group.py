import unittest
from src.game import Game, Group
from src.utils import Stone
from tests.utils import capture1, capture2, capture3

class TestGameGroups(unittest.TestCase):
    '''
    Test case for group interactions,
    including their existence and their liberties
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
        self.assertTrue(group.has_liberty((3, 2)))
        self.assertTrue(group.has_liberty((3, 4)))
        self.assertTrue(group.has_liberty((2, 3)))
        self.assertTrue(group.has_liberty((4, 3)))
        self.assertEqual(group.num_liberties, 4)
        self.assertEqual(group.num_removed_liberties, 0)

        # side of board - 3 liberties
        self.game.place_white(3, 0)
        group = self.game.gm._get_group(3, 0)
        self.assertTrue(group.has_liberty((4, 0)))
        self.assertTrue(group.has_liberty((2, 0)))
        self.assertTrue(group.has_liberty((3, 1)))
        self.assertEqual(group.num_liberties, 3)
        self.assertEqual(group.num_removed_liberties, 0)

        # corner of board - 2 liberties
        self.game.place_black(0, 0)
        group = self.game.gm._get_group(0, 0)
        self.assertTrue(group.has_liberty((0, 1)))
        self.assertTrue(group.has_liberty((1, 0)))
        self.assertEqual(group.num_liberties, 2)
        self.assertEqual(group.num_removed_liberties, 0)

    def test__merge(self):

        # place adjacent black stones and have the two groups merge into the same one
        self.game.place_black(4, 1)
        self.game.place_black(4, 2)
        self.assertTrue(self.game.gm.is_same_group(4, 1, 4, 2))
        black_group = self.game.gm._get_group(4, 1)
        self.assertTrue(black_group.has_liberty((3, 1)))
        self.assertTrue(black_group.has_liberty((3, 2)))
        self.assertTrue(black_group.has_liberty((5, 1)))
        self.assertTrue(black_group.has_liberty((5, 2)))
        self.assertTrue(black_group.has_liberty((4, 0)))
        self.assertTrue(black_group.has_liberty((4, 3)))
        self.assertEqual(black_group.num_liberties, 6)
        self.assertEqual(black_group.num_removed_liberties, 0)

        # place an adjacent, opposite colour stone does not merge
        # black group has its liberties decremented
        self.game.place_white(4, 3)
        self.assertTrue(self.game.gm.is_same_group(4, 1, 4, 2))
        black_group = self.game.gm._get_group(4, 1)
        self.assertTrue(black_group.has_liberty((3, 1)))
        self.assertTrue(black_group.has_liberty((3, 2)))
        self.assertTrue(black_group.has_liberty((5, 1)))
        self.assertTrue(black_group.has_liberty((5, 2)))
        self.assertTrue(black_group.has_liberty((4, 0)))
        self.assertEqual(black_group.num_liberties, 5)
        self.assertTrue(black_group.has_removed_liberty((4, 3)))
        self.assertEqual(black_group.num_removed_liberties, 1)

        # new white group has only 3 liberties
        white_group = self.game.gm._get_group(4, 3)
        self.assertTrue(white_group.has_liberty((4, 4)))
        self.assertTrue(white_group.has_liberty((3, 3)))
        self.assertTrue(white_group.has_liberty((5, 3)))
        self.assertEqual(white_group.num_liberties, 3)
        self.assertIn((4, 2), white_group.removed_liberties)
        self.assertEqual(white_group.num_removed_liberties, 1)

    def test__capture1(self):
        capture1(self.game)

        black_group = self.game.gm._get_group(4, 4)
        self.assertIsNone(black_group)

        self.assertFalse(self.game.gm.is_same_group(4, 5, 4, 3))
        self.assertFalse(self.game.gm.is_same_group(4, 5, 3, 4))
        self.assertFalse(self.game.gm.is_same_group(4, 5, 5, 4))
        self.assertFalse(self.game.gm.is_same_group(4, 3, 3, 4))
        self.assertFalse(self.game.gm.is_same_group(4, 3, 5, 4))
        self.assertFalse(self.game.gm.is_same_group(3, 4, 5, 4))

        white_group1 = self.game.gm._get_group(4, 5)
        self.assertTrue(white_group1.has_liberty((4, 6)))
        self.assertTrue(white_group1.has_liberty((4, 4)))
        self.assertTrue(white_group1.has_liberty((3, 5)))
        self.assertTrue(white_group1.has_liberty((5, 5)))
        self.assertEqual(white_group1.num_liberties, 4)

        white_group2 = self.game.gm._get_group(4, 3)
        self.assertTrue(white_group2.has_liberty((4, 4)))
        self.assertTrue(white_group2.has_liberty((4, 2)))
        self.assertTrue(white_group2.has_liberty((3, 3)))
        self.assertTrue(white_group2.has_liberty((5, 3)))
        self.assertEqual(white_group2.num_liberties, 4)

        white_group3 = self.game.gm._get_group(3, 4)
        self.assertTrue(white_group3.has_liberty((3, 5)))
        self.assertTrue(white_group3.has_liberty((3, 3)))
        self.assertTrue(white_group3.has_liberty((2, 4)))
        self.assertTrue(white_group3.has_liberty((4, 4)))
        self.assertEqual(white_group3.num_liberties, 4)

        white_group4 = self.game.gm._get_group(5, 4)
        self.assertTrue(white_group4.has_liberty((5, 5)))
        self.assertTrue(white_group4.has_liberty((5, 3)))
        self.assertTrue(white_group4.has_liberty((4, 4)))
        self.assertTrue(white_group4.has_liberty((6, 4)))
        self.assertEqual(white_group4.num_liberties, 4)

    def test__capture2(self):
        capture2(self.game)
        self.assertIsNone(self.game.gm._get_group(4, 3))
        self.assertIsNone(self.game.gm._get_group(4, 4))
        self.assertIsNone(self.game.gm._get_group(3, 4))

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
        self.assertTrue(white_group1.has_liberty((3, 4)))
        self.assertTrue(white_group1.has_liberty((2, 5)))
        self.assertTrue(white_group1.has_liberty((1, 4)))

        white_group2 = self.game.gm._get_group(3, 3)
        self.assertTrue(white_group2.has_liberty((3, 2)))
        self.assertTrue(white_group2.has_liberty((3, 4)))
        self.assertTrue(white_group2.has_liberty((2, 3)))
        self.assertTrue(white_group2.has_liberty((4, 3)))

        white_group3 = self.game.gm._get_group(4, 2)
        self.assertTrue(white_group3.has_liberty((3, 2)))
        self.assertTrue(white_group3.has_liberty((5, 2)))
        self.assertTrue(white_group3.has_liberty((4, 1)))
        self.assertTrue(white_group3.has_liberty((4, 3)))

        white_group4 = self.game.gm._get_group(5, 3)
        self.assertTrue(white_group4.has_liberty((5, 2)))
        self.assertTrue(white_group4.has_liberty((5, 5)))
        self.assertTrue(white_group4.has_liberty((4, 3)))
        self.assertTrue(white_group4.has_liberty((4, 4)))
        self.assertTrue(white_group4.has_liberty((6, 3)))
        self.assertTrue(white_group4.has_liberty((6, 4)))

        white_group5 = self.game.gm._get_group(3, 5)
        self.assertTrue(white_group5.has_liberty((3, 4)))
        self.assertTrue(white_group5.has_liberty((3, 6)))
        self.assertTrue(white_group5.has_liberty((4, 4)))
        self.assertTrue(white_group5.has_liberty((4, 6)))
        self.assertTrue(white_group5.has_liberty((2, 5)))
        self.assertTrue(white_group5.has_liberty((5, 5)))

    def test__capture3(self):
        capture3(self.game)
        self.assertIsNone(self.game.gm._get_group(4, 4))

        white_group1 = self.game.gm._get_group(3, 3)
        self.assertTrue(self.game.gm.is_same_group(3, 3, 4, 3))
        self.assertTrue(self.game.gm.is_same_group(3, 3, 3, 4))

        white_group2 = self.game.gm._get_group(5, 5)
        self.assertTrue(self.game.gm.is_same_group(5, 5, 5, 4))
        self.assertTrue(self.game.gm.is_same_group(5, 5, 4, 5))
        
        self.assertTrue(white_group1.has_liberty((2, 3)))
        self.assertTrue(white_group1.has_liberty((2, 4)))
        self.assertTrue(white_group1.has_liberty((3, 5)))
        self.assertTrue(white_group1.has_liberty((4, 4)))
        self.assertTrue(white_group1.has_liberty((5, 3)))
        self.assertTrue(white_group1.has_liberty((4, 2)))
        self.assertTrue(white_group1.has_liberty((3, 2)))

        self.assertTrue(white_group2.has_liberty((3, 5)))
        self.assertTrue(white_group2.has_liberty((4, 4)))
        self.assertTrue(white_group2.has_liberty((5, 3)))
        self.assertTrue(white_group2.has_liberty((6, 4)))
        self.assertTrue(white_group2.has_liberty((6, 5)))
        self.assertTrue(white_group2.has_liberty((5, 6)))
        self.assertTrue(white_group2.has_liberty((4, 6)))
