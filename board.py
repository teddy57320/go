import numpy as np
from utils import Stone

class Board(object):

    def __init__(self, config):
        self.board_size = config['board_size']
        self.black_stone_render = config['black_stone']
        self.white_stone_render = config['white_Stone']
        self.board = np.zeros((self.board_size, self.board_size))

    def place_black(self, y, x):
        self.board[y][x] = Stone.BLACK

    def place_white(self, y, x):
        self.board[y][x] = Stone.WHITE

    def value_to_printed(self, x):
        if x == Stone.EMPTY:
            return ' '
        if x == Stone.BLACK:
            return self.black_stone_render
        if x == Stone.WHITE:
            return self.white_stone_render

    def render_board(self):
        for row in range(self.board_size):
            board_row = map(self.value_to_printed, self.board[row])
            print(board_row)
