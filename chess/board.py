'''
Contains all of the information for an instance of the game.
'''

from pieces import Rook, Knight, Bishop, Queen, Pawn, King, Piece
from copy import copy,deepcopy

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
        self.pieces_white = []
        self.pieces_black = []
        self.set_initial_state()
        self.enpassant = None

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
                    board_transposed[i][j] = "."
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
    def get_piece_attack_moves(self, coord, turn):
        ''' Get all of the attack possible moves from a piece
            Assumes there is piece.
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
            #white
            if piece.color == 0:
                #Move
                #if self.board[x][y+1] is None:
                #    possible_moves.append((coord, (x,y+1)))
                #    if not piece.moved and self.board[x][y+2] is None:
                #        possible_moves.append((coord, (x, y+2)))
                #Hit
                if self.inbound((x-1,y+1)):
                    left_hit:Piece = self.board[x-1][y+1]
                    if left_hit is not None and left_hit.color != turn:
                        possible_moves.append((coord, (x+1,y+1)))
                if self.inbound((x+1, y+1)):
                    right_hit:Piece = self.board[x+1][y+1]
                    if right_hit is not None and right_hit.color != turn:
                        possible_moves.append((coord, (x-1,y+1)))

            #black
            elif not piece.color:
                if self.inbound((x-1,y-1)):
                    left_hit:Piece = self.board[x-1][y-1]
                    if left_hit is not None and left_hit.color != turn:
                        possible_moves.append((coord, (x+1,y-1)))
                if self.inbound((x+1, y-1)):
                    right_hit:Piece = self.board[x+1][y-1]
                    if right_hit is not None and right_hit.color != turn:
                        possible_moves.append((coord, (x-1,y-1)))

        return possible_moves

    def get_piece_moves(self, coord, turn):
        ''' Get all of the possible moves from a piece
            Assumes there is piece.
            Only Normal normals, No castling, en-passant.
        '''
        x = coord[0]
        y = coord[1]
        piece: Piece = self.board[x][y]
        if piece.color != turn:
            return []
        attack_moves = self.get_piece_attack_moves(coord, turn)
        possible_moves = []
        if type(piece) is Pawn:
            #white
            if piece.color:
                #Move
                if self.board[x][y+1] is None:
                    possible_moves.append((coord, (x,y+1)))
                    if not piece.moved and self.board[x][y+2] is None:
                        possible_moves.append((coord, (x, y+2)))
            #black
            if not piece.color:
                #Move
                if self.board[x][y-1] is None:
                    possible_moves.append((coord, (x,y-1)))
                    if not piece.moved and self.board[x][y-2] is None:
                        possible_moves.append((coord, (x, y-2)))
        return possible_moves + attack_moves

    def get_all_moves(self, turn):
        ''' Get all of the possible normal moves from a piece
        '''
        allmoves = []
        for i in range(8):
            for j in range(8):
                coord = (i,j)
                if self.is_piece(coord):
                    allmoves += self.get_piece_moves(coord, turn)
        return allmoves

    def get_all_legal_moves(self, turn):
        allmoves = self.get_all_moves(self,turn)
        legalmoves = []
        board_copy = deepcopy(self.board)
        for (current, next) in allmoves:
            try :
                board_copy.move(current, next, turn)
                legalmoves += (current,next)
                board_copy = deepcopy(self.board)
            except:
                pass

    def move(self, current_square, next_square, turn):
        '''
        Executes a Normal Move
        returns (taken piece, itself if pawn reach last row), otherwise return None
        '''
        #Check is in all moves
        if (current_square,next_square) not in self.get_all_moves(turn):
            raise Exception("Illegal move")

        piece = self.board[current_square[0]][current_square[1]]
        self.board[current_square[0]][current_square[1]] = None
        taken_piece = self.board[next_square[0]][next_square[1]]
        self.board[next_square[0]][next_square[1]] = piece
        if (self.is_checced(self, turn)):
            raise Exception("Illegal move, you are checked")
        #Set enpassent flag
        if type(piece) is Pawn and abs(current_square[1] - next_square[1]) == 2:
            self.enpassant = next_square
        #Assume rule pawns removed last row
        #white
        if turn and type(piece) is Pawn and next_square[1] == 7:
            return (taken_piece, piece)
        #black
        if not turn and type(piece) is Pawn and next_square[1] == 0:
            return (taken_piece, piece)
        return (taken_piece, None)

    def castle(self, small, turn):
        #todo add legatity
        #King is at (turn,4)
        row = 7 if turn else 0
        if small:
            king:King = self.board[row][4]
            rook:Rook = self.board[row][7]
            if not king.moved and not rook.moved:
                self.board[row][6] = king
                self.board[row][5] = rook
            #Big
        else:
            king:King = self.board[row][4]
            rook:Rook = self.board[row][0]
            if not king.moved and not rook.moved:
                self.board[row][2] = king
                self.board[row][3] = rook

    def check_enpassant(self, current_field, turn):
        return self.enpassant and (current_field in [[self.enpassant[0]-1, self.enpassant[1]],
                                                 [self.enpassant[0]+1, self.enpassant[1]]]) \
                                and self.board[self.enpassant[0]][self.enpassant[1]].color != \
                                    self.board[current_field[0]][current_field[1]].color

    def move_enpassant(self, current_field, turn):
        dy = 1 if turn else -1

        if self.check_enpassant(current_field, turn):
            return_piece = self.board[self.enpassant[0]][self.enpassant[1]]
            self.board[self.enpassant[0]][self.enpassant[1]] = None
            self.board[self.enpassant[0]][self.enpassant[1]+dy] = self.board[current_field[0]][current_field[1]]
            self.board[current_field[0]][current_field[1]] = None

            return return_piece

        else: raise Exception("Illegal enpassant move!")

    def is_field_attacked(self, coord, color):
        #is_field_attacked(self, (5,5), False) checks if black is attacked on F6
        attacced = False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                attacced = not (piece == None) and ((row,col),coord) in self.get_piece_attack_moves(self, (row,col), not color)
                if attacced:
                    return attacced
        return attacced

    def is_checced(self, color):
        #is_checced(self, 0) checks if black is in check
        self.is_field_attacked(self, self.find_king(self,color),color)

    def find_king(self, name, color):
        for row in range(8):
            for col in range(8):
                if self.is_piece(self, (row,col)) and self.board[row][col].abbr == "K" and self.board[row][col].color == color:
                    return (row,col)
        raise Exception("Bro idk what you have done, but apperantley there is one king missing")

    def checkmate(self, color):
        #checkmate(self, 0) is true if black mated white

        return False

if __name__ == '__main__':
    b = Board()
    print(b)
