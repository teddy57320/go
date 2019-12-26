from board import Board
from utils import Stone, make_2d_array
import numpy as np

class Group(object):
    def __init__(self, stone, liberties=None):
        if liberties is None:
            liberties = set()
        self.liberties = liberties
        self.stone = stone
        self._group = self

    @property
    def num_liberties(self):
        return len(self.liberties)

    @property
    def group(self):
        g = self
        stack = []
        while g != g._group:
            stack.append(g)
            g = g._group
        new_group = g
        for g in stack:
            g._group = new_group

        return new_group

    @staticmethod
    def merge(stone, groups, liberties=None):
        liberties = liberties or set()
        seen_groups = set()
        for g in groups:
            
            '''
            error out if we are merging different color stones
            or if we are merging groups that are already together
            '''
            assert(g == g.group)
            assert(g.stone == stone)
            assert(g not in seen_groups)
            seen_groups.add(g)

            liberties |= g.liberties

        new_group = Group(stone, liberties=liberties)
        return new_group

    def assign_group(self, g):
        self._group = g

    def __str__(self):
        return f'{super().__str__()}, liberties: {self.liberties}'


class GroupManager(object):
    def __init__(self, board):
        self.board = board
        board_size = board.board_size
        self._group_map = make_2d_array(board_size, board_size)

    def _get_group(self, y, x):
        g = self._group_map[y][x]
        if g is None:
            return g
        new_g = g.group
        if g != new_g:
            self._group_map[y][x] = new_g
        return new_g

    def merge_groups(self, y, x):
        groups = []
        stone = self.board[y][x]
        ncoords = self.board.get_neighbour_coordinates(y, x)
        liberties = set()

        for ny, nx in ncoords:
            if self.board[ny][nx] != stone:
                continue
            g = self._get_group(ny, nx)
            if g is None:
                liberties.add((ny, nx))
            else:
                groups.append(g)

        new_group = Group.merge(stone, groups, liberties=liberties)
        new_group.liberties.discard((y, x))
        
        for g in groups:
            g.assign_group(new_group)
        self._group_map[y][x] = new_group


class Game(object):
    def __init__(self, config):
        self.board = Board(config)
        self.board_size = config['board_size']
        self.moves = []
        self.gm = GroupManager(self.board)

    def undo_last_move(self):
        if not self.moves:
            return
        y, x = self.moves.pop()
        self.board[y][x] = Stone.EMPTY

    def place_black(self, y, x):
        self._place_stone(Stone.BLACK, y, x)

    def place_white(self, y, x):
        self._place_stone(Stone.WHITE, y, x)

    def _place_stone(self, stone, y, x):
        if stone == Stone.EMPTY:
            return
        self.board.place_stone(stone, y, x)
        self.gm.merge_groups(y, x)

    def render_board(self):
        self.board._render()
