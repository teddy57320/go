from src.board import Board
from src.utils import Stone, make_2d_array, get_opposite_stone
from src.exceptions import SelfDestructException, KoException
import numpy as np

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
            
            '''
            error out if we are merging different color stones
            '''
            assert(g == g.group)
            assert(g.stone == stone)

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
        board_size = board.board_size
        self._group_map = make_2d_array(board_size, board_size)
        self.captured_groups = set()
        self.num_captured_stones = {
            Stone.WHITE: 0,
            Stone.BLACK: 0
        }
        self.ko = None
        self.enable_self_destruct = enable_self_destruct

    def _get_group(self, y, x):
        g = self._group_map[y][x]
        if g is None:
            return g
        new_g = g.group
        if g != new_g:
            self._group_map[y][x] = new_g
        return new_g

    def _process_capture(self, group):
        if group.num_liberties > 0:
            return False
        self.captured_groups.add(group)
        return True

    def _check_ko(self, y, x, captured):
        if len(captured) == 1:
            cy, cx = captured[0]
            captured_group = self._get_group(cy, cx)
            if (cy, cx) == self.ko:
                self.undo_stone(y, x)
                raise KoException('You may not repeat the last board state. Please choose a different move')
            if captured_group.num_coords == 1:
                self.ko = (y, x)
        else:
            self.ko = None

    def _check_self_destruct(self, y, x, new_group):
        self_destruct = self._process_capture(new_group)
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
                self.captured_groups.discard(group)
    
        self.board.remove_stone(y, x)

    def resolve_groups(self, y, x):
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
                is_captured = self._process_capture(g)
                if is_captured:
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

        return True

    def update_state(self):

        for g in self.captured_groups:

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
            self.num_captured_stones[g.stone] += g.num_coords

        self.captured_groups.clear()


class Game(object):
    def __init__(self, config):
        self.board = Board(config)
        self.board_size = config['board_size']
        self.moves = []
        self.gm = GroupManager(self.board, enable_self_destruct=config['enable_self_destruct'])
        self.count_pass = 0

    def undo_last_move(self):
        if not self.moves:
            return
        y, x = self.moves.pop()
        self.board[y, x] = Stone.EMPTY        

    def place_black(self, y, x):
        self._place_stone(Stone.BLACK, y, x)

    def place_white(self, y, x):
        self._place_stone(Stone.WHITE, y, x)

    def pass_turn(self):
        self.count_pass += 1

    def is_over(self):
        return self.count_pass >= 2
    
    def is_within_bounds(self, y, x):
        return self.board.is_within_bounds(y, x)

    def _place_stone(self, stone, y, x):
        if stone == Stone.EMPTY:
            return
        self.count_pass = 0
        self.board.place_stone(stone, y, x)

        try:
            self.gm.resolve_groups(y, x)
        except SelfDestructException as e:
            self.board.remove_stone(y, x)
            raise e
        except KoException as e:
            self.board.remove_stone(y, x)
            raise e
            
        self.gm.update_state()

    @property
    def num_black_captured(self):
        return self.gm.num_captured_stones[Stone.BLACK]

    @property
    def num_white_captured(self):
        return self.gm.num_captured_stones[Stone.WHITE]

    def render_board(self):
        self.board._render()

    def get_scores(self):

        scores = {Stone.BLACK: 0,
                  Stone.WHITE: 0
                 }
        traversed = make_2d_array(self.board_size, self.board_size, default=lambda: False)
        for y in range(self.board_size):
            for x in range(self.board_size):
                if not traversed[y][x] and self.board[y, x] == Stone.EMPTY:
                    score, stone = self._traverse_territory(y, x, traversed)
                    if stone is not None and stone != Stone.EMPTY:
                        scores[stone] += score

        scores[Stone.BLACK] -= self.num_black_captured
        scores[Stone.WHITE] -= self.num_white_captured
        return scores

    def _traverse_territory(self, y, x, traversed):
        traversed[y][x] = True
        search = [(y, x)]
        stone = None
        count = 1
        is_neutral = False

        while search:
            y, x = search.pop()
            for ly, lx in self.board.get_liberty_coords(y, x):
                this_stone = self.board[ly, lx]
                if this_stone != Stone.EMPTY:
                    stone = stone or this_stone
                    if stone != this_stone:
                        is_neutral = True                
                if not traversed[ly][lx]:
                    if this_stone == Stone.EMPTY:
                        count += 1
                        search.append((ly, lx))
                traversed[ly][lx] = True

        if is_neutral:
            return 0, Stone.EMPTY
        return count, stone


class GameUI(object):
    def __init__(self,config):
        self.game = Game(config)
        self.turn = Stone.BLACK

    def play(self):
        
        while not self.game.is_over():
            is_turn_over = False
            self.game.render_board()

            while not is_turn_over:
                move = self._prompt_move()
                if move == 'pass':
                    self.game.pass_turn()
                    is_turn_over = True
                else:
                    is_turn_over = self._place_stone(move)

            self._switch_turns()

        self._display_result()

    def _display_result(self):
        scores = self.game.get_scores()
        black_score = scores[Stone.BLACK]
        white_score = scores[Stone.WHITE]

        print(f'Black score: {black_score}')
        print(f'White score: {white_score}')

        if black_score == white_score:
            print('The result is a tie!')
        else:
            winner = Stone.BLACK if black_score > white_score else Stone.WHITE
            winner = self._get_player_name(winner)
            print(f'The winner is {winner}!')        

    def _place_stone(self, move):
        y, x = move
        try:
            if self.turn == Stone.BLACK:
                self.game.place_black(y, x)
            elif self.turn == Stone.WHITE:
                self.game.place_white(y, x)
            is_turn_over = True
        except Exception as e:
            print(e)
            is_turn_over = False
        return is_turn_over

    def _get_player_name(self, stone):
        return 'Black' if stone == Stone.BLACK else 'White'

    def _switch_turns(self):
        self.turn = Stone.BLACK if self.turn == Stone.WHITE else Stone.WHITE
        
    def _prompt_move(self):
        move = None
        player = self._get_player_name(self.turn)
        while not self._is_valid_move(move):
            print('Please input a valid move (enter "pass" or a coordinate)')
            move = input(f'{player} move: ')
        
        return self._parse_move(move)
    
    def _is_valid_move(self, move):
        if move == 'pass':
            return True
        try:
            y, x = self._parse_coordinates(move)
            return self.game.is_within_bounds(y, x)
        except:
            return False

    def _parse_coordinates(self, move):
        y, x = move.split(' ')
        return int(y), int(x)
    
    def _parse_move(self, move):
        if move == 'pass':
            return move
        return self._parse_coordinates(move)
