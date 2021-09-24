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
        # 0 is white
        self.color = None
        #Tuples of direction change
        self.moves = []
        self.abbr = "N"
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
        self.abbr = "K"
class Pawn(Piece):
    def __init__(self, color):
        super(Pawn, self).__init__()
        self.color = color
        self.straight = False
        self.diag = False
        self.moved = False
        #self.moves base moves
        if self.color == 0:
            self.moves = [(0,1), (-1,1), (1,1) ]
        else:
            self.moves = [(0, -1), (-1, -1), (1, -1)]
        self.abbr = "P"
    def getMoves(self):
        #white
        if not self.moved:
            if self.color == 0:
                return self.moves + [(0,2)]
            else:
                return self.moves + [(0,-2)]
        else:
            return self.moves

class King(Piece):
    def __init__(self, color):
        self.color = color
        super(King, self).__init__()
        self.moves = [(-1,-1), (1,1), (-1,1), (1,-1), (0,1), (0,-1), (1,0), (-1,1)]
        self.abbr = "K"