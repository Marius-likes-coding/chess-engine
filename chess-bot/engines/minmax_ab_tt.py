import chess
from .evaluate import evaluate_position
from .game_data import GameData
from .transposition_table import TranspositionTable

INF = 10000000
DEFAULT_DEPTH = 4

tt = TranspositionTable()


def search_move(game_data, depth=DEFAULT_DEPTH):
    best_move = None
    best_value = -INF
    alpha = -INF
    beta = INF
    legal_moves = list(game_data.board.legal_moves)

    for move in legal_moves:
        game_data.push_move(move)
        value = min_max(game_data, depth - 1, alpha, beta, False)
        game_data.pop_move()

        if value > best_value:
            best_move = move
            best_value = value

        alpha = max(alpha, value)

    return best_move


def min_max(game_data, depth, alpha, beta, is_maximizing_player):

    _hash = game_data.zobrist_hash.h()
    stored = tt.get_node(_hash)
    if stored is not None and stored.depth >= depth:
        if stored.kind == "exact":
            return stored.value
        elif stored.kind == "alpha":  # upper bound
            beta = min(beta, stored.value)
        elif stored.kind == "beta":  # lower bound
            alpha = max(alpha, stored.value)
        # if stored.depth >= 0: examine stored move first

    legal_moves = list(game_data.board.legal_moves)

    if depth == 0 or len(legal_moves) == 0:
        sign = 1 if game_data.color == chess.WHITE else -1
        return sign * evaluate_position(game_data)

    if is_maximizing_player:
        value = -1000000
        current_alpha = alpha  #
        for move in legal_moves:
            game_data.push_move(move)
            value = max(
                value, min_max(game_data, depth - 1, current_alpha, beta, False)
            )
            game_data.pop_move()

            current_alpha = max(current_alpha, value)  # upper bound
            if value >= beta:
                break

    else:
        value = +1000000
        for move in legal_moves:
            game_data.push_move(move)
            value = min(value, min_max(game_data, depth - 1, alpha, beta, True))
            game_data.pop_move()

            beta = min(beta, value)  # lower bound
            if value <= alpha:
                break

    if alpha < value and value < beta:
        tt.insert_node(_hash, "", value, "exact", depth)
    elif value <= alpha:
        tt.insert_node(_hash, "", value, "alpha", depth)
    elif value >= beta:
        tt.insert_node(_hash, "", value, "beta", depth)

    return value