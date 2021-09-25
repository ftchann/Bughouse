'''
Contains all of the information for an instance of the game.
'''

from pieces import Rook, Knight, Bishop, Queen, Pawn, King, Piece


class Board:
    '''
    Stores boardstate of game.
    '''
    def __init__(self):
        '''
        Sets up all of the pieces that are initially on the board
        when the game starts
        '''
        self.board = [[Piece]]
        self.board = [[None for x in range(8)] for y in range(8)]
        #Pieces to place in
        self.pieces = []
        self.set_initial_state()
        self.enpassent = None
    def set_initial_state(self):
        #0 is white
        self.board[0][0] = Rook(0)
        self.board[1][0] = Knight(0)
        self.board[2][0] = Bishop(0)
        self.board[3][0] = Queen(0)
        self.board[4][0] = King(0)
        self.board[5][0] = Bishop(0)
        self.board[6][0] = Knight(0)
        self.board[7][0] = Rook(0)
        for i in range(8):
            self.board[i][1] = Pawn(0)
        #Black
        self.board[0][7] = Rook(1)
        self.board[1][7] = Knight(1)
        self.board[2][7] = Bishop(1)
        self.board[3][7] = Queen(1)
        self.board[4][7] = King(1)
        self.board[5][7] = Bishop(1)
        self.board[6][7] = Knight(1)
        self.board[7][7] = Rook(1)
        for i in range(8):
            self.board[i][6] = Pawn(1)
    def __str__(self):
        answer = ""
        board_transposed = [list(x) for x in zip(*self.board)]
        for i in range(8):
            for j in range(8):
                if board_transposed[i][j] is None:
                    board_transposed[i][j] = "E"
        for i in board_transposed:
            answer += ('\t'.join(map(str, i))) + "\n"
        return answer
    def inbound(self, coord):
        x = coord[0]
        y = coord[1]
        if 0 <= x and x <= 7 and 0 <= y and y <= 7:
            return True
        else:
            return False
    def is_piece(self, coord):
        x = coord[0]
        y = coord[1]
        if self.board[x][y] is not None:
            return True
        else:
            return False
    def get_piece_moves(self, coord, turn):
        ''' Get all of the possible moves from a piece
            Only Normal normals, No castling enpassent.
        '''

        x = coord[0]
        y = coord[1]
        piece: Piece = self.board[x][y]
        if piece.color != turn:
            return []
        #(oldpos, newpos)
        possible_moves = []
        #None Pawns aka Knights, King
        for move in piece.getMoves():
            newpos = (x + move[0], y + move[1])
            if self.inbound(newpos):
                piece_at_new_pos = self.board[newpos[0]][newpos[1]]
                if piece_at_new_pos is None or piece_at_new_pos.color != turn:
                    possible_moves.append((coord, newpos))
        def add_new_pos(newpos, possible_moves):
            #Not inbound break instantly
            if not self.inbound(newpos):
                return True
            piece_at_new_pos = self.board[newpos[0]][newpos[1]]
            if piece_at_new_pos is None:
                possible_moves.append((coord, newpos))
                return False
            elif piece_at_new_pos.color != turn:
                possible_moves.append((coord, newpos))
                return True
            else:
                return True
        if piece.straight:
            #Left
            for i in range(1,7):
                newpos = (x - i, y)
                tobreak = add_new_pos(newpos, possible_moves)
                if tobreak:
                    break
            #Right
            for i in range(1,7):
                newpos = (x - i, y)
                tobreak = add_new_pos(newpos, possible_moves)
                if tobreak:
                    break
            #Up
            for i in range(1,7):
                newpos = (x, y+i)
                tobreak = add_new_pos(newpos, possible_moves)
                if tobreak:
                    break
            #Down
            for i in range(1,7):
                newpos = (x, y-i)
                tobreak = add_new_pos(newpos, possible_moves)
                if tobreak:
                    break
        if piece.diag:
            #Left Down
            for i in range(1,7):
                newpos = (x-i, y-i)
                tobreak = add_new_pos(newpos, possible_moves)
                if tobreak:
                    break
            #Right Down
            for i in range(1,7):
                newpos = (x+i, y-i)
                tobreak = add_new_pos(newpos, possible_moves)
                if tobreak:
                    break
            #Left Up
            for i in range(1,7):
                newpos = (x-i, y+i)
                tobreak = add_new_pos(newpos, possible_moves)
                if tobreak:
                    break
            #Right up
            for i in range(1,7):
                newpos = (x+i, y+i)
                tobreak = add_new_pos(newpos, possible_moves)
                if tobreak:
                    break
        #Pawn
        if type(piece) is Pawn:
            if piece.color == 0:
                #Move
                if self.board[x][y+1] is None:
                    possible_moves.append((coord, (x,y+1)))
                    if not piece.moved and self.board[x][y+2] is None:
                        possible_moves.append((coord, (x, y+2)))
                #Hit
                left_hit:Piece = self.board[x-1][y+1]
                right_hit:Piece = self.board[x-1][y+1]
                if right_hit is not None and right_hit.color != turn:
                    possible_moves.append((coord, (x-1,y+1)))
                if left_hit is not None and left_hit.color != turn:
                    possible_moves.append((coord, (x+1,y+1)))
    def get_all_moves(self, turn):
        ''' Get all of the possible normal moves from a piece
        '''
        allmoves = []
        for i in range(8):
            for j in range(8):
                coord = (i,j)
                if self.is_piece(self, coord):
                    allmoves += self.get_piece_moves(coord, turn)
        return allmoves


b = Board()
print(b)