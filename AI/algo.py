from copy import deepcopy
import pygame


BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLUE, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def simulate_move(piece, move, table, skip):
    table.movepiece(piece, move[0], move[1])
    if skip:
        table.remove(skip)

    return table


def get_all_moves(table, color, game):
    moves = []

    for piece in table.get_all_pieces(color):
        valid_moves = table.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_table = deepcopy(table)
            temp_piece = temp_table.getpiece(piece.ligne, piece.col)
            new_table = simulate_move(temp_piece, move, temp_table, game, skip)
            moves.append(new_table)

    return moves


