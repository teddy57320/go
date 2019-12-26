class Stone:
    EMPTY = 0
    BLACK = 1
    WHITE = 2

def make_2d_array(h, w, default=lambda: None):
    return [[default() for i in range(w)] for j in range(h)]
