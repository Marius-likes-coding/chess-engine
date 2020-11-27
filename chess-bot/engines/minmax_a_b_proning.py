import chess
from .evaluate import evaluate_position
from .game_data import GameData

INF = 10000000


def a_b_min_max_first_iteration(game_data, depth, is_maximizing_player):
    best_move = None
    best_value = -INF
    alpha = -INF
    beta = INF

    for move in game_data.board.legal_moves:
        game_data.board.push(move)
        value = min_max(game_data, depth - 1, alpha, beta, False)
        game_data.board.pop()

        if value > best_value:
            best_move = move
            best_value = value

        alpha = max(alpha, value)

    return best_move


def min_max(game_data, depth, alpha, beta, is_maximizing_player):
    legal_moves = list(game_data.board.legal_moves)

    if depth == 0 or len(legal_moves) == 0:
        sign = 1 if game_data.color == chess.WHITE else -1
        return sign * evaluate_position(game_data)

    elif is_maximizing_player:
        value = -1000000
        for move in legal_moves:
            game_data.board.push(move)
            value = max(value, min_max(game_data, depth - 1, alpha, beta, False))
            game_data.board.pop()

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return value

    else:
        value = +1000000
        for move in legal_moves:
            game_data.board.push(move)
            value = min(value, min_max(game_data, depth - 1, alpha, beta, True))
            game_data.board.pop()

            beta = min(beta, value)
            if alpha >= beta:
                break

        return value


# fen = "r1b1kb1r/pp1n1ppp/2pq1n2/3p2N1/4p3/3N4/PPPPPPPP/R1BQKB1R w KQkq - 0 9"


# def print_score_of_fen(fen):
#     game_data = GameData(1)
#     game_data.board = chess.Board(fen)
#     game_data.color = chess.WHITE
#     move3 = min_max_first_iteration(game_data, 3, True)
#     print(f"move3: {move3}")
#     move4 = min_max_first_iteration(game_data, 4, True)
#     print(f"move4: {move4}")


# print_score_of_fen(fen)
