import pygame
from thegame.var import WIDTH, HEIGHT, SZ, WHITE
from thegame.game import Game
from AI.algo import minimax


T = 60
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('JEU DE DAMES')

def getmousepos(pos):
    x, y = pos
    ligne = y // SZ
    col = x // SZ
    return ligne, col

def main():
    game1 = Game(SCREEN)
    game = True
    clock = pygame.time.Clock()

    while game:
        clock.tick(T)

        if game1.turn == WHITE:
            value, new_table = minimax(game1.get_table(), 3, WHITE, game1)
            game1.ai_move(new_table)

        if game1.winner() != None:
            print(game.winner())
            game = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                ligne, col = getmousepos(pos)
                game1.select(ligne, col)



        game1.update()


    pygame.quit()

main()






