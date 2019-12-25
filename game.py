from board import Board

class Game(object):
    def __init__(self, config):
        self.board = Board(config)
        self.board_size = config['board_size']

    def _check_win(self, y, x):
        '''
        To check if a piece placed at (y, x) results in a win, we only need to 
        check the 9x9 pixel patch centered at (y, x)
        '''
        window = 9
        # todo

