import unittest
from src.game import Game, Group
from src.utils import Stone
from src.exceptions import SelfDestructException, KoException

def capture1(game):
    '''
    Case of capture where white captures black as follows
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][ ][ ][ ]
    3 [ ][ ][ ][ ][w][ ][ ]
    4 [ ][ ][ ][w][b][w][ ]
    5 [ ][ ][ ][ ][w][ ][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    game.place_black(4, 4)
    game.place_white(4, 5)
    game.place_white(4, 3)
    game.place_white(3, 4)
    game.place_white(5, 4)

def capture2(game):
    '''
    Case of capture where white captures black as follows
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][w][ ][ ]
    3 [ ][ ][ ][w][b][w][ ]
    4 [ ][ ][w][b][b][w][ ]
    5 [ ][ ][ ][w][w][ ][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    for y, x in [(4, 3), (3, 4), (4, 4)]:
        game.place_black(y, x)
    for y, x in [(2, 4), (3, 3), (4, 2), (5, 3), (5, 4), (4, 5), (3, 5)]:
        game.place_white(y, x)

def capture3(game):
    '''
    Case of capture where white captures black as follows
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][ ][ ][ ]
    3 [ ][ ][ ][w][w][ ][ ]
    4 [ ][ ][ ][w][b][w][ ]
    5 [ ][ ][ ][ ][w][w][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    game.place_black(4, 4)
    game.place_white(4, 5)
    game.place_white(4, 3)
    game.place_white(3, 4)
    game.place_white(3, 3)
    game.place_white(5, 5)
    game.place_white(5, 4)

def self_destruct1(game):
    '''
    Case of self destruct where, given the following board, black places at (4, 4)
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][ ][ ][ ]
    3 [ ][ ][ ][ ][w][ ][ ]
    4 [ ][ ][ ][w][b][w][ ]
    5 [ ][ ][ ][ ][w][ ][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    game.place_white(4, 5)
    game.place_white(4, 3)
    game.place_white(3, 4)
    game.place_white(5, 4)
    game.place_black(4, 4)

def self_destruct2(game):
    '''
    Case of self destruct where, given the following board, black places at (4, 3), (3, 4), (4, 4)
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][w][ ][ ]
    3 [ ][ ][ ][w][b][w][ ]
    4 [ ][ ][w][b][b][w][ ]
    5 [ ][ ][ ][w][w][ ][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    for y, x in [(2, 4), (3, 3), (4, 2), (5, 3), (5, 4), (4, 5), (3, 5)]:
        game.place_white(y, x)
    for y, x in [(4, 3), (3, 4), (4, 4)]:
        game.place_black(y, x)

def self_destruct3(game):
    '''
    Case of self destruct where, given the following board, black places at (3, 3)
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][w][w][w][w][w][ ]
    2 [ ][w][b][b][b][w][ ]
    3 [ ][w][b][ ][b][w][ ]
    4 [ ][w][b][b][b][w][ ]
    5 [ ][w][w][w][w][w][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]

    the result is 
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][w][w][w][w][w][ ]
    2 [ ][w][ ][ ][ ][w][ ]
    3 [ ][w][ ][ ][ ][w][ ]
    4 [ ][w][ ][ ][ ][w][ ]
    5 [ ][w][w][w][w][w][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    for y, x in [(2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (3, 2)]:
        game.place_black(y, x)
    for y, x in [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 5), (3, 5), (4, 5), (5, 5),
                 (5, 4), (5, 3), (5, 2), (5, 1),
                 (4, 1), (3, 1), (2, 1)]:
        game.place_white(y, x)

    game.place_black(3, 3)


class TestGame(unittest.TestCase):
    '''
    Test agent for game logic testing from user interface
    Tests involve stone placements only
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
        '''
        Basic stone placing logic
        '''

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


class TestGameGroups(unittest.TestCase):
    '''
    Test the underlying logic of groups, including their existence and their liberties
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
        '''
        Groups obtained by simply placing stones
        '''

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


class TestScore(unittest.TestCase):
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
