from src.board import Board
from src.utils import Stone, make_2d_array, get_opposite_stone
import numpy as np

class Group(object):
    def __init__(self, stone, liberties=None, coords=None):
        self.liberties = liberties or set()
        self.coords = coords or set()
        self.stone = stone
        self._group = self

    @property
    def num_liberties(self):
        return len(self.liberties)

    @property
    def group(self):
        g = self
        stack = []
        while g is not None and g != g._group:
            stack.append(g)
            g = g._group
        new_group = g
        for g in stack:
            g._group = new_group

        return new_group

    @staticmethod
    def merge(stone, groups, merge_coord, liberties=None):
        liberties = liberties or set()
        coords = set()
        for g in groups:
            
            '''
            error out if we are merging different color stones
            '''
            assert(g == g.group)
            assert(g.stone == stone)

            liberties |= g.liberties
            coords |= g.coords

        new_group = Group(stone, liberties=liberties, coords=coords)
        new_group.liberties.discard(merge_coord)
        new_group.coords.add(merge_coord)
        return new_group

    def assign_group(self, g):
        self._group = g

    def __str__(self):
        return f'{super().__str__()},\nliberties: {self.liberties},\ncoords: {self.coords}'


class GroupManager(object):
    def __init__(self, board):
        self.board = board
        board_size = board.board_size
        self._group_map = make_2d_array(board_size, board_size)
        self.captured_groups = set()

    def _get_group(self, y, x):
        g = self._group_map[y][x]
        if g is None:
            return g
        new_g = g.group
        if g != new_g:
            self._group_map[y][x] = new_g
        return new_g

    def resolve_groups(self, y, x):
        groups = set()
        stone = self.board[y][x]
        opposite_stone = get_opposite_stone(stone)
        ncoords = self.board.get_neighbour_coordinates(y, x)
        liberties = set()

        for ny, nx in ncoords:
            g = self._get_group(ny, nx)

            if self.board[ny][nx] == Stone.EMPTY:
                liberties.add((ny, nx))

            elif self.board[ny][nx] == opposite_stone:
                g.liberties.discard((y, x))
                if g.num_liberties <= 0:
                    g.assign_group(None)
                    self.captured_groups.add(g)

            else:
                groups.add(g)

        new_group = Group.merge(stone, groups, (y, x), liberties=liberties)
        
        for g in groups:
            g.assign_group(new_group)
        self._group_map[y][x] = new_group

    def update_board(self):
        for g in self.captured_groups:
            for y, x in g.coords:
                self.board[y][x] = Stone.EMPTY
                self._group_map[y][x] = None
        self.captured_groups.clear()


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
        self.gm.resolve_groups(y, x)
        self.gm.update_board()

    def render_board(self):
        self.board._render()
