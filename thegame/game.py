import pygame
from .var import WHITE, BLUE, SZ
from.table import Table


class Game:
    def __init__(self, screen):
        self._init()
        self.screen = screen

    def update(self):
        self.table.finaltable(self.screen)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.table = Table()
        self.turn = BLUE
        self.valid_moves = {}

    def winner(self):
        return self.table.winner()

    def reset(self):
        self._init()

    def select(self, lign, col):
        if self.selected:
            result = self._move(lign, col)
            if not result:
                self.selected = None
                self.select(lign, col)

        piece = self.table.getpiece(lign, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.table.get_valid_moves(piece)
            return True

        return False

    def _move(self, lign, col):
        piece = self.table.getpiece(lign, col)
        if self.selected and piece == 0 and (lign, col) in self.valid_moves:
            self.table.movepiece(self.selected, lign, col)
            skipped = self.valid_moves[(lign, col)]
            if skipped:
                self.table.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            lign, col = move
            pygame.draw.circle(self.screen, (255, 0, 0),
                               (col * SZ + SZ // 2, lign * SZ + SZ // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLUE:
            self.turn = WHITE
        else:
            self.turn = BLUE

    def get_table(self):
        return self.table

    def ai_move(self, table):
        self.table = table
        self.change_turn()