import pygame


class Piece:

    def __init__(self, color: str, pos: tuple):

        self.color = color

        self.pos = [pos[0], pos[1]]  # Makes sure that pos is list

    def move(self, dest, board=None):
        """Move the piece to coordinates (x, y) specified in 'dest'."""

        self.pos[0], self.pos[1] = dest[0], dest[1]

        self.update_moves(board)

    def draw(self, surface, size, *pos):
        """Draw the piece to chosen pygame-surface."""

        if not pos:
            pos = (self.pos[0] * size, self.pos[1] * size)

        self.sprite = pygame.transform.scale(self.sprite, (size, size))
        self.sprite = pygame.transform.scale(self.sprite, (size, size))
        surface.blit(self.sprite, pos)


class Bishop(Piece):

    def __init__(self, color, pos):
        super().__init__(color, pos)

        self.sprite = pygame.image.load(color + "Bishop.png")

        self.update_moves()

    def update_moves(self, board=None):

        self.moves = []

        x, y = self.pos[0], self.pos[1]

        for i in [x for x in range(-7, 8) if x != 0]:
            self.moves.append([x + i, y + i])
            self.moves.append([x + i, y - i])

        if board:
            self.remove_diag_blocks(board)

    def remove_diag_blocks(self, board):

        x, y = self.pos[0], self.pos[1]

        for i in [a for  a in range(1, 8) if x + a < 8 and y + a < 8]:
            if board[x + i][y + i]:
                for j in range(i + 1, 8):
                    if x + i > 7 or y + i > 7:
                        break
                    try:
                        self.moves.remove([x + j, y + j])
                    except ValueError:
                        continue

        for i in [a for  a in range(1, 8) if x + a < 8 and y - a >= 0]:
            if board[x + i][y - i]:
                for j in range(i + 1, 8):
                    if x + i > 7 or y - i >= 7:
                        break
                    try:
                        self.moves.remove([x + j, y - j])
                    except ValueError:
                        continue

        for i in [a for a in range(1, 8) if x - a >= 0 and y + a < 8]:
            if board[x - i][y + i]:
                for j in range(i + 1, 8):
                    if x - j < 0 or y + j > 7:
                        break
                    try:
                        self.moves.remove([x - j, y + j])
                    except ValueError:
                        continue

        for i in [a for a in range(1, 8) if x - a >= 0 and y - a >= 0]:
            if board[x - i][y - i]:
                for j in range(i + 1, 8):
                    if x - i < 0 or y - i < 0:
                        break
                    try:
                        self.moves.remove([x - j, y - j])
                    except ValueError:
                        continue


class Rook(Piece):

    def __init__(self, color, pos):
        super().__init__(color, pos)

        self.sprite = pygame.image.load(color + "Rook.png")

        self.update_moves()

    def update_moves(self, board=None):

        self.moves = []

        x, y = self.pos[0], self.pos[1]

        for i in [x for x in range(-8, 8) if x != 0]:
            self.moves.append([x + i, y])
            self.moves.append([x, y + i])

        if board:
            self.remove_straight_blocks(board)

    def remove_straight_blocks(self, board):

        x, y = self.pos[0], self.pos[1]

        for i in range(1, 8 - x):
            if board[x + i][y]:
                for j in range(i + 1, 8 - x):
                    try:
                        self.moves.remove([x + j, y])
                    except ValueError:
                        continue

        for i in range(1, x + 1):
            if board[x - i][y]:
                for j in range(i + 1, x + 1):
                    try:
                        self.moves.remove([x - j, y])
                    except ValueError:
                        continue

        for i in range(1, 8 - y):
            if board[x][y + i]:
                for j in range(i + 1, 8 - y):
                    try:
                        self.moves.remove([x, y + j])
                    except ValueError:
                        continue

        for i in range(1, y + 1):
            if board[x][y - i]:
                for j in range(i + 1, y + 1):
                    try:
                        self.moves.remove([x, y - j])
                    except ValueError:
                        continue


class Pawn(Piece):

    def __init__(self, color, pos):
        super().__init__(color, pos)

        self.sprite = pygame.image.load(color + "Pawn.png")

        self.first_move = True

        self.update_moves()

    def update_moves(self, board=None):

        self.moves = []

        dy = {"white": -1, "black": 1}[self.color]
        self.moves.append([self.pos[0], self.pos[1] + dy])
        if self.first_move:
            self.moves.append([self.pos[0], self.pos[1] + 2 * dy])

        if board:
            for square in self.moves:
                x, y = square[0], square[1]
                if board[x][y]:
                    self.moves.remove(square)

            x, y = self.pos[0], self.pos[1]
            for dx in [-1, 1]:
                try:
                    if board[x + dx][y + dy]:
                        if board[x + dx][y + dy].color != self.color:
                            self.moves.append([x + dx, y + dy])
                except IndexError:
                    continue



    def move(self, dest, board=None):
        super().move(dest)

        self.first_move = False


class Queen(Rook, Bishop):

    def __init__(self, color, pos):

        super().__init__(color, pos)

        self.sprite = pygame.image.load(color + "Queen.png")

        self.update_moves()

    def update_moves(self, board=None):

        x, y = self.pos[0], self.pos[1]

        self.moves = []

        for i in [x for x in range(-7, 8) if x != 0]:
            self.moves.append([x + i, y + i])
            self.moves.append([x + i, y - i])
            self.moves.append([x + i, y])
            self.moves.append([x, y + i])

        if board:
            self.remove_diag_blocks(board)
            self.remove_straight_blocks(board)


class Knight(Piece):

    def __init__(self, color, pos):
        super().__init__(color, pos)

        self.sprite = pygame.image.load(color + "Knight.png")

        self.update_moves()

    def update_moves(self, board=None):

        x, y = self.pos[0], self.pos[1]

        self.moves = [[x - 1, y - 2], [x + 1, y - 2], [x + 2, y - 1],
                      [x + 2, y + 1], [x + 1, y + 2], [x - 1, y + 2],
                      [x - 2, y + 1], [x - 2, y - 1]]

        # Removing moves which end on friendly piece.
        # if board:
        #     for move in temp_moves:
        #         if 0 <= move[0] < 8 and 0 <= move[1] < 8:
        #             if not board[move[0]][move[1]]:
        #                 self.moves.append(move)
        #             elif board[move[0]][move[1]].color != self.color:
        #                 self.moves.append(move)

class King(Piece):

    def __init__(self, color, pos):
        super().__init__(color, pos)

        self.sprite = pygame.image.load(color + "King.png")

        self.update_moves()

    def update_moves(self, board=None):

        x, y = self.pos[0], self.pos[1]

        # Temporary list of moves, will be filtered below.
        self.moves = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x + 1, y],
                      [x + 1, y + 1], [x, y + 1], [x - 1, y + 1], [x - 1, y]]

        # # Removing moves which end on friendly piece or outside the board.
        # if board:
        #     for move in temp_moves:
        #         if 0 <= move[0] < 8 and 0 <= move[1] < 8:
        #             if not board[move[0]][move[1]]:
        #                 self.moves.append(move)
        #             elif board[move[0]][move[1]].color != self.color:
        #                 self.moves.append(move)

if __name__ == "__main__":
    # For testing purposes

    test = Piece("white", (0, 0))

    screen = pygame.display.set_mode((500, 500))
    test.draw(screen, 50)
