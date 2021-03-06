'''
Contains all of the different pieces in the game
as well as a base 'Piece' class
'''

class Piece:
    '''
    Superclass for piece type.
    '''
    def __init__(self):
        self.straight = False
        self.diag = False
        # True is white
        self.color = None
        #Tuples of direction change
        self.moves = []
        self.abbr = "^"
    def getMoves(self):
        return self.moves

    def __str__(self):
        return self.abbr

class Queen(Piece):
    def __init__(self, color):
        super(Queen, self).__init__()
        self.color = color
        self.straight = True
        self.diag = True
        self.abbr = "Q"

class Rook(Piece):
    def __init__(self, color):
        super(Rook, self).__init__()
        self.color = color
        self.straight = True
        self.abbr = "R"
        self.moved = False

class Bishop(Piece):
    def __init__(self, color):
        super(Bishop, self).__init__()
        self.color = color
        self.diag = True
        self.abbr = "B"

class Knight(Piece):
    def __init__(self, color):
        super(Knight, self).__init__()
        self.color = color
        self.moves = [(-2,-1), (-1,-2), (1,-2), (2,-1), (2,1), (1,2), (-1,2), (-2,1)]
        self.abbr = "N"

class Pawn(Piece):
    def __init__(self, color):
        super(Pawn, self).__init__()
        self.abbr = "P"
        self.color = color
        self.straight = False
        self.diag = False
        self.moved = False

class King(Piece):
    def __init__(self, color):
        super(King, self).__init__()
        self.color = color
        self.moves = [(-1,-1), (1,1), (-1,1), (1,-1), (0,1), (0,-1), (1,0), (-1,1)]
        self.abbr = "K"
        self.moved = False
