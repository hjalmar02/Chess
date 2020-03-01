import pygame
from sys import exit
import sys
from os.path import join
from pieces import *

WS = (1000, 1000)  # Window size (x, y)

# Size of board squares
TILESIZE = WS[0] // 8

BLACK = (0, 0, 0)

# Board colors
LIGHTBROWN = (222, 184, 135)
BROWN = (139, 69, 19)


class ChessGame:

    def __init__(self):

        self.board = []
        for column in range(8):  # Two-dimensional list, eight rows and columns
            self.board.append([None] * 8)  # 'None' represents an empty square

        self.selected = None

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

        if self.selected:

            # Marking all possible moves for selected piece. Each move is represented
            # by a transparent circle
            marker = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
            center = (TILESIZE // 2, TILESIZE // 2)
            radius = TILESIZE // 4
            pygame.draw.circle(marker, (0, 0, 0, 100), center, radius)
            for square in self.selected.moves:
                x, y = square[0], square[1]
                x *= TILESIZE
                y *= TILESIZE
                surface.blit(marker, (x, y))

            # Draw selected piece on mouse cursor
            pos = [i - TILESIZE // 2 for i in pygame.mouse.get_pos()]
            self.selected.draw(surface, TILESIZE, pos)

        # Drawing all other (non-selected) pieces
        for column in self.board:
            for piece in column:
                if piece:
                    if piece != self.selected:
                        piece.draw(surface, TILESIZE)

    def set_board(self):

        # Black pieces
        self.board[0][0] = Rook("black", (0, 0))
        self.board[1][0] = Knight("black", (1, 0))
        self.board[2][0] = Bishop("black", (2, 0))
        self.board[3][0] = Queen("black", (3, 0))
        self.board[4][0] = King("black", (4, 0))
        self.board[5][0] = Bishop("black", (5, 0))
        self.board[6][0] = Knight("black", (6, 0))
        self.board[7][0] = Rook("black", (7, 0))
        for column in range(8):
            self.board[column][1] = Pawn("black", (column, 1))

        # White pieces
        self.board[0][7] = Rook("white", (0, 7))
        self.board[1][7] = Knight("white", (1, 7))
        self.board[2][7] = Bishop("white", (2, 7))
        self.board[3][7] = Queen("white", (3, 7))
        self.board[4][7] = King("white", (4, 7))
        self.board[5][7] = Bishop("white", (5, 7))
        self.board[6][7] = Knight("white", (6, 7))
        self.board[7][7] = Rook("white", (7, 7))
        for column in range(8):
            self.board[column][6] = Pawn("white", (column, 6))

    def play(self):

        self.set_board()

        pygame.init()
        screen = pygame.display.set_mode(WS)

        # Main loop
        while True:
            screen.fill(BLACK)

            for column in self.board:
                for piece in column:
                    if piece:
                        piece.update_moves(self.board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.selected = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = [i // TILESIZE for i in pygame.mouse.get_pos()]
                    if not self.selected:
                        self.selected = self.board[x][y]
                    else:
                        if [x, y] == self.selected.pos:
                            self.selected = None
                        elif [x, y] in self.selected.moves:

                            prevx = self.selected.pos[0]
                            prevy = self.selected.pos[1]

                            self.selected.move((x, y), self.board)
                            self.board[x][y] = self.selected
                            self.selected = None
                            self.board[prevx][prevy] = None

            self.draw(screen)

            pygame.display.update()


if __name__ == "__main__":
    a = ChessGame()
    a.play()
