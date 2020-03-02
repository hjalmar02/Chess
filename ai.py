from random import choice


class ChessBot:

    def __init__(self, color):

        self.color = color

        self.pieces = []

    def random_move(self, board):

        made_move = False

        self.pieces = []

        for column in board:
            for piece in column:
                if piece != None:
                    #print(piece, '\n')
                    if piece.color == self.color:
                        #print(f"{piece}\n{piece.color}\n")
                        self.pieces.append(piece)

        while True:
            piece = choice(self.pieces)
            if len(piece.moves) > 0:
                break
        

        move = choice(piece.moves)

        #print(f"{piece}\n{piece.color}, {piece.pos}-{move}\n")

        return piece.pos, move

