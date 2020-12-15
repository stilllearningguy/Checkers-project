import pygame
from .var import LIGN, COL, BLACK, WHITE, BLUE, SZ
from .piece import Piece




class Table:

    def __init__(self):
        self.table = []
        self.whiteleft = self.blueleft = 12
        self.whiteking = self.blueking = 0
        self.remptable()


    def drawtable(self, screen):
        screen.fill(BLACK)
        for ligne in range(LIGN):
            for col in range(ligne % 2, COL, 2):
                pygame.draw.rect(screen, WHITE, (ligne*SZ, col*SZ, SZ, SZ))

    def movepiece(self, piece, ligne, col):
        self.table[piece.ligne][piece.col], self.table[ligne][col] = self.table[ligne][col], self.table[piece.ligne][piece.col]
        piece.move(ligne, col)

        if ligne == LIGN - 1 or ligne == 0:
            piece.king()
            if piece.color == BLUE:
                self.whiteking += 1
            else:
                self.blueking += 1


    def evaluate(self):
        return self.whiteleft - self.blueleft + (self.whiteking * 0.5 - self.blueking * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for lign in self.table:
            for piece in lign:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)



    def getpiece(self, ligne, col):
        return self.table[ligne][col]



    def remptable(self):
        for ligne in range(LIGN):
            self.table.append([])
            for col in range(COL):
                if ligne % 2 == 0:
                    if col % 2 != 0:
                        if ligne < 3:
                            self.table[ligne].append(Piece(ligne, col, WHITE))
                        elif ligne > 4:
                            self.table[ligne].append(Piece(ligne, col, BLUE))
                        else:
                            self.table[ligne].append(0)
                    else:
                        self.table[ligne].append(0)
                if ligne % 2 != 0:
                    if col % 2 == 0:
                        if ligne < 3:
                            self.table[ligne].append(Piece(ligne, col, WHITE))
                        elif ligne > 4:
                            self.table[ligne].append(Piece(ligne, col, BLUE))
                        else:
                            self.table[ligne].append(0)
                    else:
                        self.table[ligne].append(0)

    def finaltable(self, screen):
        self.drawtable(screen)
        for ligne in range(LIGN):
            for col in range(COL):
                p = self.table[ligne][col]
                if p != 0:
                    p.drawp(screen)


    def remove(self, pieces):
        for piece in pieces:
            self.table[piece.ligne][piece.col] = 0
            if piece != 0:
                if piece.color == BLUE:
                    self.blueleft -= 1
                else:
                    self.whiteleft -= 1


    def winner(self):
        if self.blueleft <= 0:
            return WHITE
        elif self.whiteleft <= 0:
            return BLUE


    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        ligne = piece.ligne
        if piece.color == BLUE or piece.isking:
            moves.update(self._traverse_left(ligne - 1, max(ligne - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(ligne - 1, max(ligne - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.isking:
            moves.update(self._traverse_left(ligne + 1, min(ligne + 3, LIGN), 1, piece.color, left))
            moves.update(self._traverse_right(ligne + 1, min(ligne + 3, LIGN), 1, piece.color, right))


        return moves


    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.table[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        ligne = max(r-3, 0)
                    else:
                        ligne = min(r+3, LIGN)
                    moves.update(self._traverse_left(r+step, ligne, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, ligne, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COL:
                break

            current = self.table[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        ligne = max(r - 3, 0)
                    else:
                        ligne = min(r + 3, LIGN)
                    moves.update(self._traverse_left(r + step, ligne, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, ligne, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right +=1
        return moves