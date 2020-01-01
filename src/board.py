import numpy as np
from src.utils import Stone

class Board(np.ndarray):

    def __new__(cls, config={}):

        board_size = config['board_size']
        shape = (board_size, board_size)
        obj = super(Board, cls).__new__(cls, shape, dtype=np.int)

        obj.board_size = board_size
        obj.black_stone_render = config['black_stone']
        obj.white_stone_render = config['white_stone']

        obj.fill(Stone.EMPTY)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.board_size = getattr(obj, 'board_size')
        self.black_stone_render = getattr(obj, 'black_stone_render')
        self.white_stone_render = getattr(obj, 'white_stone_render')

    def get_liberty_coords(self, y, x):
        coords = []
        if y > 0:
            coords.append((y-1, x))
        if y < self.board_size-1:
            coords.append((y+1, x))
        if x > 0:
            coords.append((y, x-1))
        if x < self.board_size-1:
            coords.append((y, x+1))
        return coords

    def place_stone(self, stone, y, x):
        self[y][x] = stone

    def remove_stone(self, y, x):
        self[y][x] = Stone.EMPTY

    def is_within_bounds(self, y, x):
        return 0 <= y <= self.board_size and 0 <= x <= self.board_size

    def _value_to_render(self, x):
        s = None
        if x == Stone.EMPTY:
            s = ' '
        elif x == Stone.BLACK:
            s = self.black_stone_render
        elif x == Stone.WHITE:
            s = self.white_stone_render
        return f'[{s}]'

    def _render(self):
        print('\n   ' + '  '.join([self._index_to_label(x) \
                            for x in range(self.board_size)]))
        for row in range(self.board_size):
            label = self._index_to_label(row)
            board_row = map(self._value_to_render, self[row])
            print(f'{label} ' + ''.join(board_row))
        print('')

    def _index_to_label(self, idx):
        if idx < 10:
            return str(idx)
        return chr(idx - 10 + ord('A'))
