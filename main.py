import pygame
from sys import exit
import sys
from os.path import join
from pieces import *
from ai import ChessBot
from math import sqrt

WS = (1000, 1000)  # Window size (x, y)

# Size of board squares
TILESIZE = WS[0] // 8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (0, 255, 255)


# Board colors
LIGHTBROWN = (222, 184, 135)
BROWN = (139, 69, 19)

DEBUG = False


class ChessGame:

    def __init__(self):

        pygame.init()

        self.board = []
        for column in range(8):  # Two-dimensional list, eight rows and columns
            self.board.append([None] * 8)  # 'None' represents an empty square

        self.selected = None

        self.font = pygame.font.Font('freesansbold.ttf', int(0.060 * WS[0]))

        # "AI" opponent (currently only random movements)
        self.opp = ChessBot("black")

    @staticmethod
    def check_quit():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self, surface, selection=True):

        # Draw board background
        for column in range(0, 8):
            for row in range(0, 8):
                x, y = column * TILESIZE, row * TILESIZE
                w, h = TILESIZE, TILESIZE
                if row % 2 == column % 2:
                    pygame.draw.rect(surface, LIGHTBROWN, (x, y, w, h))
                else:
                    pygame.draw.rect(surface, BROWN, (x, y, w, h))

        if self.selected and selection:

            # Marker for possible moves.
            marker = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
            center = (TILESIZE // 2, TILESIZE // 2)
            radius = TILESIZE // 4

            for square in self.selected.moves:
                x, y = square[0], square[1]

                # If the king is selected, illegal moves (that would
                # leave it in check) are marked.
                if isinstance(self.selected, King):
                    if self.selected.color == "white":
                        if square in self.black_moves:
                            # Red marker = Illegal move
                            pygame.draw.circle(
                                marker, (255, 0, 0, 100), center, radius)
                        else:
                            if 0 <= x < 8 and 0 <= y < 8:
                                if (self.board[x][y]
                                        and self.board[x][y].color == self.selected.color):
                                    continue
                                pygame.draw.circle(
                                    marker, (0, 0, 0, 100), center, radius)
                    elif self.selected.color == "black":
                        if square in self.white_moves:
                            pygame.draw.circle(
                                marker, (255, 0, 0, 100), center, radius)
                        else:
                            if 0 <= x < 8 and 0 <= y < 8:
                                if (self.board[x][y]
                                        and self.board[x][y].color == self.selected.color):
                                    continue
                            pygame.draw.circle(
                                marker, (0, 0, 0, 100), center, radius)

                # The king isn't selected
                else:
                    if 0 <= x < 8 and 0 <= y < 8:
                        # Unmarking all friendly pieces
                        if (self.board[x][y]
                                and self.board[x][y].color == self.selected.color):
                            continue
                        else:
                            pygame.draw.circle(
                                marker, (0, 0, 0, 100), center, radius)
                    else:
                        continue

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

        # Emptying board
        for column in self.board:
            for square in column:
                square = None

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

    def move_selected(self, dest, animate=False):
        """Move selected piece to destination, if possible."""

        x, y = dest[0], dest[1]

        if self._legal_move(dest):
            prevx = self.selected.pos[0]
            prevy = self.selected.pos[1]
            if not animate:
                self.selected.move((x, y), self.board)
                self.board[x][y] = self.selected
            else:
                startx = prevx * TILESIZE
                starty = prevy * TILESIZE
                print(startx, starty)

                endx = x * TILESIZE
                endy = y * TILESIZE
                dx, dy = endx - startx, endy - starty

                steps = int(sqrt(dx ** 2 + dy ** 2) / 10)

                for i in range(steps):
                    pygame.time.delay(10)
                    self.check_quit()
                    x_ani = startx + int(i / steps * (endx - startx))
                    y_ani = starty + int(i / steps * (endy - starty))
                    self.draw(self.screen, False)
                    self.selected.draw(self.screen, TILESIZE, (x_ani, y_ani))
                    pygame.display.update()

                self.selected.move((x, y), self.board)
                self.board[x][y] = self.selected


            self.selected = None
            self.board[prevx][prevy] = None
            self.cur_turn = {
            "white": "black", "black": "white"
            }[self.cur_turn]


    def is_checkmate(self):
        """Check if either king is in checkmate."""
        white_checkmate = True
        black_checkmate = True

        for column in self.board:
            for piece in column:
                if piece and isinstance(piece, King):
                    if piece.color == "white":
                        if piece.pos in self.black_moves:
                            white_checkmate = True
                            for move in piece.moves:
                                if move not in self.black_moves:
                                    if (self.board[move[0]][move[1]] and
                                        self.board[move[0]][move[1]].color 
                                            != piece.color):
                                        white_checkmate = False
                                    elif not self.board[move[0]][move[1]]:
                                        white_checkmate = False
                            if white_checkmate:
                                self.loser = "WHITE"
                                self.game_over = True

        for column in self.board:
            for piece in column:
                if piece and isinstance(piece, King):
                    if piece.color == "black":
                        if piece.pos in self.white_moves:
                            black_checkmate = True
                            for move in piece.moves:
                                if move not in self.white_moves:
                                    try:
                                        if (self.board[move[0]][move[1]] and # TODO: Raises errors
                                            self.board[move[0]][move[1]].color 
                                                != piece.color):
                                            black_checkmate = False
                                        elif not self.board[move[0]][move[1]]:
                                            black_checkmate = False
                                    except IndexError:
                                        continue
                            if black_checkmate:
                                self.loser = "BLACK"
                                self.game_over = True

    def game_over_screen(self, surface, loser=None):

        for alpha in range(0, 25):
            self.check_quit()
            pygame.time.delay(50)
            overlay = pygame.Surface(WS, pygame.SRCALPHA)
            self.draw(overlay)
            overlay.fill((0, 0, 0, alpha))
            surface.blit(overlay, (0, 0))
            pygame.display.update()

        for alpha in range(0, 100):
            pygame.time.delay(30)
            text_srfc = pygame.Surface(WS, pygame.SRCALPHA)
            text = self.font.render(f"{loser} IS IN CHECKMATE!", True, (0, 255, 255))
            x, y = WS[0] // 8, WS[1] // 2 - 1 / 4 * WS[1]
            text_srfc.blit(text, (x, y))

            text2 = self.font.render("PRESS [R] TO RESTART", True, (0, 255, 255))
            x, y = WS[0] // 8, WS[1] // 2
            text_srfc.blit(text2, (x, y))

            surface.blit(text_srfc, (0, 0))
            pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.set_board()
                        self.play()
                        break
            pygame.display.update()

    def _legal_move(self, dest):
        """Check if move to dest with selected piece is legal.

        Args:
            dest (tuple/list): Move destination (x, y).

        Returns:
            bool: True if move is legal, False if not.

        """
    
        x, y = dest[0], dest[1]

        color = self.selected.color

        opp_moves = {
        "white": self.black_moves, "black": self.white_moves
        }[color]

        if not 0 <= x < 8 or not 0 <= y < 8:
            print('invalid index')
            return False

        # Check if move is in selected piece's range
        if [x, y] in self.selected.moves:

            # Friendly piece on square
            if self.board[x][y] and self.board[x][y].color == color:
                return False

            # Square is empty or occupied by opponent piece.
            else:

                # King is selected => check for enemy moves
                if isinstance(self.selected, King):
                    # King would be in check
                    if [x, y] in opp_moves:
                        return False
                return True
        else:
            return False

        


    def play(self):

        self.set_board()

        pygame.init()
        self.screen = pygame.display.set_mode(WS)

        # Current turn ("white"/"black")
        self.cur_turn = "white"

        self.game_over = False
        self.loser = None
        # Main loop
        while not self.game_over:
            
            self.screen.fill(BLACK)

            # All possible movements of the white and black pieces,
            # respectively.
            self.white_moves = []
            self.black_moves = []

            for column in self.board:
                for piece in column:
                    if piece:
                        piece.update_moves(self.board)
                        if piece.color == "white":
                            for square in piece.moves:
                                self.white_moves.append(square)

                            if isinstance(piece, Pawn):
                                x, y = piece.pos[0], piece.pos[1]
                                self.white_moves.append(
                                    [[x - 1, y - 1], [x + 1, y - 1]])
                                try:
                                    self.white_moves.remove([x, y - 2])
                                except ValueError:
                                    pass
                        elif piece.color == "black":
                            if isinstance(piece, Pawn):
                                x, y = piece.pos[0], piece.pos[1]
                                self.black_moves.append([x - 1, y + 1])
                                self.black_moves.append([x + 1, y + 1])
                            else:
                                for square in piece.moves:
                                    self.black_moves.append(square)

            self.is_checkmate()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # ESC-key deselects your current piece
                    if event.key == pygame.K_ESCAPE:
                        self.selected = None
                    if event.key == pygame.K_END and DEBUG:
                        self.game_over = True

                # Pressed mousebutton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # The (x, y)-coordinates for the square you pressed:
                    x, y = [i // TILESIZE for i in pygame.mouse.get_pos()]

                    if not self.selected:
                        if self.board[x][y]:
                            if self.board[x][y].color == self.cur_turn or DEBUG:
                                # Selects piece on clicked square
                                self.selected = self.board[x][y]
                    else:
                        # If you pressed the original position of your
                        # selected piece it will deselect it
                        if [x, y] == self.selected.pos:
                            self.selected = None

                        # Square is a valid move
                        elif [x, y] in self.selected.moves:

                            # King is selected
                            if isinstance(self.selected, King):
                                if self.selected.color == "white":
                                    if [x, y] not in self.black_moves:
                                        self.move_selected((x, y))
                                elif self.selected.color == "black":
                                    if [x, y] not in self.white_moves:
                                        self.move_selected((x, y))
                            else:
                                self.move_selected((x, y))

            if self.cur_turn == "black":
                while True:
                    opp_move = self.opp.random_move(self.board)
                    xpos, ypos = opp_move[0]
                    x, y = opp_move[1]
                    self.selected = self.board[xpos][ypos]

                    if self._legal_move((x, y)):
                        
                        self.move_selected((x, y), True)
                        break



            self.draw(self.screen)

            pygame.display.update()

        self.game_over_screen(self.screen, self.loser)


if __name__ == "__main__":
    a = ChessGame()
    a.play()
