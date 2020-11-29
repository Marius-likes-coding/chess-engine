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


# fen = "r2qr1k1/1pp2p2/3p3Q/p3p1N1/8/P2Rn1B1/5PPP/5RK1 b - - 0 25"


# def print_score_of_fen(fen):
#     game_data = GameData(1)
#     game_data.board = chess.Board(fen)
#     game_data.color = chess.BLACK
#     move3 = a_b_min_max_first_iteration(game_data, 5, True)
#     print(move3.uci())


# print_score_of_fen(fen)
