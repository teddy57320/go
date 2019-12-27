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

    def get_neighbour_coordinates(self, y, x):
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
        # self.moves.append((y, x))

    def _value_to_render(self, x):
        s = None
        if x == Stone.EMPTY:
            s = ' '
        if x == Stone.BLACK:
            s = self.black_stone_render
        if x == Stone.WHITE:
            s = self.white_stone_render
        return f'[{s}]'

    def _render(self):
        print('\n   ' + '  '.join([str(x) for x in range(self.board_size)]))
        for row in range(self.board_size):
            board_row = map(self._value_to_render, self[row])
            print(f'{row} ' + ''.join(board_row))
        print('')
