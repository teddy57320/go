import numpy as np
from utils import Stone

class Board(np.ndarray):

    def __new__(cls, config={}):

        board_size = config['board_size']
        shape = (board_size, board_size)
        obj = super(Board, cls).__new__(cls, shape, dtype=np.int)

        obj.board_size = board_size
        obj.black_stone_render = config['black_stone']
        obj.white_stone_render = config['white_stone']
        obj.moves = []

        obj.fill(Stone.EMPTY)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.board_size = getattr(obj, 'board_size')
        self.black_stone_render = getattr(obj, 'black_stone_render')
        self.white_stone_render = getattr(obj, 'white_stone_render')
        self.moves = getattr(obj, 'moves')

    def place_black(self, y, x):
        self._place_stone(Stone.BLACK, y, x)

    def place_white(self, y, x):
        self._place_stone(Stone.WHITE, y, x)

    def _place_stone(self, stone, y, x):
        self[y][x] = stone
        self.moves.append((y, x))

    def undo_last_move(self):
        if not self.moves:
            return
        y, x = self.moves.pop()
        self[y][x] = Stone.EMPTY

    def _value_to_render(self, x):
        s = None
        if x == Stone.EMPTY:
            s = ' '
        if x == Stone.BLACK:
            s = self.black_stone_render
        if x == Stone.WHITE:
            s = self.white_stone_render
        return f'[{s}]'

    def render_board(self):
        for row in range(self.board_size):
            board_row = map(self._value_to_render, self[row])
            print(''.join(board_row))
