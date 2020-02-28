import pygame
from sys import exit
from os.path import join

WS = (1000, 1000)  # Window size (x, y)

# Size of board squares
TILESIZE = WS[0] // 8

BLACK = (0, 0, 0)

# Board colors
LIGHTBROWN = (222, 184, 135)
BROWN = (139, 69, 19)


# Defining piece movements (change in x, change in y)
KING = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]

QUEEN = []
for i in range(-8, 8):
    QUEEN.append([i, i])
    QUEEN.append([i, 0])
    QUEEN.append([0, i])
    QUEEN.append([i, -i])

ROOK = []
for i in range(-8, 8):
    ROOK.append([0, i])
    ROOK.append([i, 0])

BISHOP = []
for i in range(-8, 8):
    BISHOP.append([i, i])
    BISHOP.append([i, -i])

PAWN = [[0, -1], [0, -2], [0, 1], [0, 2]]


class Piece:

    def __init__(self, type: str, color: str, pos: tuple):

        self.type = type
        if color != "white" and color != "black":
            raise ValueError("Invalid color, color must be 'white' or 'black'.")
        else:
            self.color = color.lower()
        self.x, self.y = pos[0], pos[1]
        self.first_move = True

        self.types = {
            "Pawn": PAWN,
            "Knight": [[-1, -2], [1, -2], [2, -1], [-2, -1], [-1, 2], [1, 2], [2, 1], [-2, 1]],
            "Queen": QUEEN,
            "Rook": ROOK,
            "King": KING,
            "Bishop": BISHOP
        }
        self.moves = []

        self.sprite = pygame.image.load(join('pieces', color + type + ".png"))
        self.sprite = pygame.transform.scale(self.sprite, (TILESIZE, TILESIZE))

    def get_moves(self, board):
        self.moves = []
        for move in self.types[self.type]:
            self.moves.append([self.x + move[0], self.y + move[1]])

        if self.type == "Pawn":
            if self.color == "white":
                self.moves.remove([self.x + 0, self.y + 1])
                self.moves.remove([self.x + 0, self.y + 2])
                if not self.first_move:
                    self.moves.remove([self.x + 0, self.y - 2])
                try:
                    if board[self.x - 1][self.y - 1]:
                        if board[self.x - 1][self.y - 1].color == "black":
                            self.moves.append([self.x - 1, self.y - 1])
                    if board[self.x + 1][self.y - 1]:
                        if board[self.x + 1][self.y - 1].color == "black":
                            self.moves.append([self.x + 1, self.y - 1])
                except IndexError:
                    pass

            elif self.color == "black":
                self.moves.remove([self.x + 0, self.y - 1])
                self.moves.remove([self.x + 0, self.y - 2])
                if not self.first_move:
                    self.moves.remove([self.x + 0, self.y + 2])
                try:
                    if board[self.x - 1][self.y + 1]:
                        if board[self.x - 1][self.y + 1].color == "white":
                            self.moves.append([self.x - 1, self.y + 1])
                    if board[self.x + 1][self.y + 1]:
                        if board[self.x + 1][self.y + 1].color == "white":
                            self.moves.append([self.x + 1, self.y + 1])
                except IndexError:
                    pass

        if self.type == "Queen":

            for i in range(1, 8):
                try:
                    if board[self.x + i][self.y + i]:
                        for j in range(i, 8):
                            try:
                                self.moves.remove([self.x + j, self.y + j])
                            except IndexError:
                                break
                            except ValueError:
                                break
                        if board[self.x + i][self.y + i].color != self.color:
                            self.moves.append([self.x + i, self.y + i])
                except IndexError:
                    break
                try:
                    if board[self.x + i][self.y - i]:
                        for j in range(i, 8):
                            try:
                                self.moves.remove([self.x + j, self.y - j])
                            except IndexError:
                                break
                            except ValueError:
                                break
                        if board[self.x + i][self.y - i].color != self.color:
                            self.moves.append([self.x + i, self.y - i])
                        break
                except IndexError:
                    break

        return self.moves

    def draw(self, surface, pos):
        x, y = pos[0], pos[1]
        surface.blit(self.sprite, (x, y))

    def move(self, dest, board):

        self.x, self.y = dest[0], dest[1]
        self.get_moves(board)
        self.first_move = False


class ChessGame:

    def __init__(self):

        self.board = []
        for column in range(8):  # Two-dimensional list, eight rows and columns
            self.board.append([None] * 8)  # 'None' represents an empty square

    def draw(self, surface):

        # Draw board background
        for column in range(0, 8):
            for row in range(0, 8):
                x, y = column * TILESIZE, row * TILESIZE
                w, h = TILESIZE, TILESIZE
                if row % 2 == column % 2:
                    pygame.draw.rect(surface, LIGHTBROWN, (x, y, w, h))
                else:
                    pygame.draw.rect(surface, BROWN, (x, y, w, h))

        if self.selected_piece:
            mouse_pos = pygame.mouse.get_pos()
            for square in self.selected_piece.moves:
                x, y = square[0], square[1]
                if 0 <= x < 8 and 0 <= y < 8:
                    # if self.board[x][y] == None:
                    x *= TILESIZE
                    y *= TILESIZE
                    highlight = pygame.Surface((TILESIZE, TILESIZE))
                    highlight.set_alpha(50)
                    highlight.fill((0, 200, 0))
                    surface.blit(highlight, (x, y))
            x = mouse_pos[0] - TILESIZE / 2
            y = mouse_pos[1] - TILESIZE / 2
            self.selected_piece.draw(surface, (x, y))

        for column in self.board:
            for piece in column:
                if piece:
                    if not piece == self.selected_piece:
                        x, y = piece.x * TILESIZE, piece.y * TILESIZE
                        piece.draw(surface, (x, y))

    def set_board(self):
        """Clear board and place new pieces."""
        for col in self.board:
            for piece in col:
                piece = None

        for x in range(8):
            self.board[x][6] = Piece("Pawn", "white", (x, 6))

        self.board[0][7] = Piece("Rook", "white", (0, 7))
        self.board[1][7] = Piece("Knight", "white", (1, 7))
        self.board[2][7] = Piece("Bishop", "white", (2, 7))
        self.board[3][7] = Piece("Queen", "white", (3, 7))
        self.board[4][7] = Piece("King", "white", (4, 7))
        self.board[5][7] = Piece("Bishop", "white", (5, 7))
        self.board[6][7] = Piece("Knight", "white", (6, 7))
        self.board[7][7] = Piece("Rook", "white", (7, 7))

        for x in range(8):
            self.board[x][1] = Piece("Pawn", "black", (x, 1))

        self.board[0][0] = Piece("Rook", "black", (0, 0))
        self.board[1][0] = Piece("Knight", "black", (1, 0))
        self.board[2][0] = Piece("Bishop", "black", (2, 0))
        self.board[3][0] = Piece("Queen", "black", (3, 0))
        self.board[4][0] = Piece("King", "black", (4, 0))
        self.board[5][0] = Piece("Bishop", "black", (5, 0))
        self.board[6][0] = Piece("Knight", "black", (6, 0))
        self.board[7][0] = Piece("Rook", "black", (7, 0))

    def play(self):
        screen = pygame.display.set_mode(WS)

        self.set_board()

        self.selected_piece = None
        current_turn = "white"

        while True:

            pygame.time.delay(50)
            screen.fill(BLACK)

            if self.selected_piece:
                self.selected_piece.get_moves(self.board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.selected_piece = None
                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()
                    # Get clicked square
                    x, y = pos[0] // TILESIZE, pos[1] // TILESIZE
                    if self.selected_piece:
                        # Check if move is valid
                        if [x, y] in self.selected_piece.moves:
                            prevx, prevy = self.selected_piece.x, self.selected_piece.y
                            # Check if there is a piece on target square
                            if self.board[x][y]:
                                if self.board[x][y] != current_turn:
                                    # Deleting opponent piece and moving
                                    self.board[x][y] = None
                                    self.selected_piece.move(
                                        (x, y), self.board)
                                    self.board[x][y] = self.selected_piece
                                    self.board[prevx][prevy] = None
                                    self.selected_piece = None
                                    if current_turn == "white":
                                        current_turn = "black"
                                    else:
                                        current_turn = "white"
                            else:
                                self.selected_piece.move((x, y), self.board)
                                self.board[x][y] = self.selected_piece
                                self.board[prevx][prevy] = None
                                self.selected_piece = None
                                if current_turn == "white":
                                    current_turn = "black"
                                else:
                                    current_turn = "white"
                    else:
                        try:
                            if self.board[x][y].color == current_turn:
                                self.selected_piece = self.board[x][y]
                        except AttributeError:  # You clicked empty square
                            pass

                    # if self.selected_piece:
                    #     if [x, y] in self.selected_piece.moves:
                    #         if self.board[x][y]:
                    #             if self.board[x][y].color == "black":
                    #                 self.board[x][y] = None
                    #         prevx = self.selected_piece.x
                    #         prevy = self.selected_piece.y
                    #         self.selected_piece.move((x, y))
                    #         self.board[x][y] = self.selected_piece
                    #         self.board[prevx][prevy]
                    #         self.selected_piece = None
                    # else:
                    #     self.selected_piece = self.board[x][y]

            self.draw(screen)
            pygame.display.update()


if __name__ == "__main__":
    a = ChessGame()
    a.play()
