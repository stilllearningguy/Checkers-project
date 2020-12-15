import pygame
from .var import BLACK, WHITE, LIGN, COL, SZ, BLUE, KING


class Piece:
    def __init__(self, ligne, col, color):
        self.ligne = ligne
        self.col = col
        self.color = color
        self.isking = False
        self.x = 0
        self.y = 0
        self.postion()

    def postion(self):
        self.y = SZ*self.ligne + 40
        self.x = SZ*self.col + 40

    def king(self):
        self.isking = True

    def drawp(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 28)
        if self.isking:
            screen.blit(KING,(self.x - 26, self.y - 25))


    def move(self, ligne, col):
        self.ligne = ligne
        self.col = col
        self.postion()



