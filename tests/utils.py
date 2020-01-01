def capture1(game):
    '''
    Case of capture where white captures black as follows
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][ ][ ][ ]
    3 [ ][ ][ ][ ][w][ ][ ]
    4 [ ][ ][ ][w][b][w][ ]
    5 [ ][ ][ ][ ][w][ ][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    game.place_black(4, 4)
    game.place_white(4, 5)
    game.place_white(4, 3)
    game.place_white(3, 4)
    game.place_white(5, 4)

def capture2(game):
    '''
    Case of capture where white captures black as follows
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][w][ ][ ]
    3 [ ][ ][ ][w][b][w][ ]
    4 [ ][ ][w][b][b][w][ ]
    5 [ ][ ][ ][w][w][ ][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    for y, x in [(4, 3), (3, 4), (4, 4)]:
        game.place_black(y, x)
    for y, x in [(2, 4), (3, 3), (4, 2), (5, 3), (5, 4), (4, 5), (3, 5)]:
        game.place_white(y, x)

def capture3(game):
    '''
    Case of capture where white captures black as follows
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][ ][ ][ ]
    3 [ ][ ][ ][w][w][ ][ ]
    4 [ ][ ][ ][w][b][w][ ]
    5 [ ][ ][ ][ ][w][w][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    game.place_black(4, 4)
    game.place_white(4, 5)
    game.place_white(4, 3)
    game.place_white(3, 4)
    game.place_white(3, 3)
    game.place_white(5, 5)
    game.place_white(5, 4)

def self_destruct1(game):
    '''
    Case of self destruct where, given the following board, black places at (4, 4)
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][ ][ ][ ]
    3 [ ][ ][ ][ ][w][ ][ ]
    4 [ ][ ][ ][w][b][w][ ]
    5 [ ][ ][ ][ ][w][ ][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    game.place_white(4, 5)
    game.place_white(4, 3)
    game.place_white(3, 4)
    game.place_white(5, 4)
    game.place_black(4, 4)

def self_destruct2(game):
    '''
    Case of self destruct where, given the following board, black places at (4, 3), (3, 4), (4, 4)
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][w][ ][ ]
    3 [ ][ ][ ][w][b][w][ ]
    4 [ ][ ][w][b][b][w][ ]
    5 [ ][ ][ ][w][w][ ][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    for y, x in [(2, 4), (3, 3), (4, 2), (5, 3), (5, 4), (4, 5), (3, 5)]:
        game.place_white(y, x)
    for y, x in [(4, 3), (3, 4), (4, 4)]:
        game.place_black(y, x)

def self_destruct3(game):
    '''
    Case of self destruct where, given the following board, black places at (3, 3)
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][w][w][w][w][w][ ]
    2 [ ][w][b][b][b][w][ ]
    3 [ ][w][b][ ][b][w][ ]
    4 [ ][w][b][b][b][w][ ]
    5 [ ][w][w][w][w][w][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]

    the result is 
       0  1  2  3  4  5  6
    0 [ ][ ][ ][ ][ ][ ][ ]
    1 [ ][w][w][w][w][w][ ]
    2 [ ][w][ ][ ][ ][w][ ]
    3 [ ][w][ ][ ][ ][w][ ]
    4 [ ][w][ ][ ][ ][w][ ]
    5 [ ][w][w][w][w][w][ ]
    6 [ ][ ][ ][ ][ ][ ][ ]
    '''
    for y, x in [(2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (3, 2)]:
        game.place_black(y, x)
    for y, x in [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 5), (3, 5), (4, 5), (5, 5),
                 (5, 4), (5, 3), (5, 2), (5, 1),
                 (4, 1), (3, 1), (2, 1)]:
        game.place_white(y, x)

    game.place_black(3, 3)
