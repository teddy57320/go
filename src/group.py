from src.utils import Stone, make_2d_array, get_opposite_stone
from src.exceptions import SelfDestructException, KoException

class Group(object):
    def __init__(self, stone, liberties=None, removed_liberties=None, coords=None):
        self.liberties = liberties or set()
        self.removed_liberties = removed_liberties or set()
        self.coords = coords or set()
        self.stone = stone
        self._group = self

    @property
    def num_liberties(self):
        return len(self.liberties)

    @property
    def num_removed_liberties(self):
        return len(self.removed_liberties)

    @property
    def num_coords(self):
        return len(self.coords)

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
    def merge(stone, groups, merge_coord, liberties=None, removed_liberties=None):
        liberties = liberties or set()
        coords = set()
        removed_liberties = removed_liberties or set()
        for g in groups:

            liberties |= g.liberties
            coords |= g.coords
            removed_liberties |= g.removed_liberties

        new_group = Group(stone, liberties=liberties,
                                 removed_liberties=removed_liberties,
                                 coords=coords)
        new_group.liberties.discard(merge_coord)
        new_group.coords.add(merge_coord)
        return new_group

    def assign_group(self, g):
        self._group = g

    def remove_liberty(self, coord):
        self.liberties.discard(coord)
        self.removed_liberties.add(coord)

    def restore_liberty(self, coord):
        self.liberties.add(coord)
        self.removed_liberties.discard(coord)

    def has_liberty(self, coord):
        return coord in self.liberties
    
    def has_removed_liberty(self, coord):
        return coord in self.removed_liberties

    def __str__(self):
        return f'{super().__str__()},\nliberties: {self.liberties},\ncoords: {self.coords}'


class GroupManager(object):
    def __init__(self, board, enable_self_destruct):
        self.board = board
        self.enable_self_destruct = enable_self_destruct

        self._group_map = make_2d_array(board.board_size, board.board_size)
        self._captured_groups = set()
        self._num_captured_stones = {
            Stone.WHITE: 0,
            Stone.BLACK: 0
        }
        self._potential_ko = None

    def _get_group(self, y, x):
        g = self._group_map[y][x]
        if g is None:
            return g
        new_g = g.group
        if g != new_g:
            self._group_map[y][x] = new_g
        return new_g

    def _is_captured(self, group):
        if group.num_liberties > 0:
            return False
        self._captured_groups.add(group)
        return True

    def _check_ko(self, y, x, captured):
        if len(captured) == 1:
            cy, cx = captured[0]
            captured_group = self._get_group(cy, cx)
            if (cy, cx) == self._potential_ko:
                self.undo_stone(y, x)
                raise KoException('You may not repeat the last board state. Please choose a different move')
            if captured_group.num_coords == 1:
                self._potential_ko = (y, x)
        else:
            self._potential_ko = None

    def _check_self_destruct(self, y, x, new_group):
        self_destruct = self._is_captured(new_group)
        if self_destruct:
            new_group.assign_group(None)
            if not self.enable_self_destruct:
                self.undo_stone(y, x)
                raise SelfDestructException('Self destruction is not permitted. Please choose a different move.')
        
    def is_same_group(self, y1, x1, y2, x2):
        return self._get_group(y1, x1) == self._get_group(y2, x2)

    def undo_stone(self, y, x):
        stone = self.board[y, x]
        opposite_stone = get_opposite_stone(stone)
        for ly, lx in self.board.get_liberty_coords(y, x):
            if self.board[ly, lx] == opposite_stone:
                group = self._get_group(ly, lx)
                group.restore_liberty((y, x))
                group.assign_group(group)
                self._captured_groups.discard(group)

        this_group = self._get_group(y, x)
        self._captured_groups.discard(this_group)
        self.board.remove_stone(y, x)

    def resolve_board(self, y, x):
        groups = set()
        stone = self.board[y, x]
        opposite_stone = get_opposite_stone(stone)
        new_group_liberties = set()
        new_group_removed_liberties = set()
        captured = []

        for ly, lx in self.board.get_liberty_coords(y, x):
            g = self._get_group(ly, lx)

            if self.board[ly, lx] == Stone.EMPTY:
                new_group_liberties.add((ly, lx))

            elif self.board[ly, lx] == opposite_stone:
                g.remove_liberty((y, x))
                if self._is_captured(g):
                    captured.append((ly, lx))
                    new_group_liberties.add((ly, lx))
                else:
                    new_group_removed_liberties.add((ly, lx))

            else:
                groups.add(g)

        self._check_ko(y, x, captured)

        new_group = Group.merge(stone, groups, (y, x),  
                                liberties=new_group_liberties,
                                removed_liberties=new_group_removed_liberties
                               )

        self._check_self_destruct(y, x, new_group)

        for g in groups:
            g.assign_group(new_group)
        self._group_map[y][x] = new_group

    def update_state(self):

        for g in self._captured_groups:

            # nullify group
            g.assign_group(None)

            # restore liberties to those who had liberties removed by a group that was captured
            for y, x in g.removed_liberties:
                group_to_change = self._get_group(y, x)
                if group_to_change is None:
                    continue
                liberty_coords = self.board.get_liberty_coords(y, x)
                for lcoord in liberty_coords:
                    if lcoord in g.coords:
                        group_to_change.restore_liberty(lcoord)

            # clear captured regions on board
            for y, x in g.coords:
                self.board.remove_stone(y, x)
                self._group_map[y][x] = None

            # record the captured groups
            self._num_captured_stones[g.stone] += g.num_coords

        self._captured_groups.clear()