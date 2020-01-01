from src.board import Board
from src.utils import Stone, make_2d_array
from src.group import Group, GroupManager
from src.exceptions import (
    SelfDestructException, KoException, InvalidInputException)

class Game(object):
    def __init__(self, config):
        self.board = Board(config)
        self.board_size = config['board_size']
        self.gm = GroupManager(self.board,
                               enable_self_destruct=config['enable_self_destruct'])
        self.count_pass = 0

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
            self.gm.resolve_board(y, x)
        except SelfDestructException as e:
            self.board.remove_stone(y, x)
            raise e
        except KoException as e:
            self.board.remove_stone(y, x)
            raise e
            
        self.gm.update_state()

    @property
    def num_black_captured(self):
        return self.gm._num_captured_stones[Stone.BLACK]

    @property
    def num_white_captured(self):
        return self.gm._num_captured_stones[Stone.WHITE]

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
        y, x = move.strip().split()
        y = self._label_to_coord(y)
        x = self._label_to_coord(x)
        return y, x
    
    def _label_to_coord(self, label):
        if label.isnumeric():
            coord = int(label)
            if coord >= 10:
                raise InvalidInputException('')
            return int(label)
        if label.isalpha() and label >= 'A':
            diff = ord(label) - ord('A')
            if diff < 0:
                raise InvalidInputException('')
            return 10 + diff
        raise InvalidInputException('')

    def _parse_move(self, move):
        if move == 'pass':
            return move
        return self._parse_coordinates(move)
