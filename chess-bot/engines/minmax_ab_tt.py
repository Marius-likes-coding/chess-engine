import chess
from .evaluate import evaluate_position
from .game_data import GameData
from .transposition_table import TranspositionTable

INF = 10000000
DEFAULT_DEPTH = 4

tt = TranspositionTable()


def tt_length():
    return len(tt)


def search_move(game_data, stats, depth=DEFAULT_DEPTH):
    best_move = None
    best_value = -INF
    alpha = -INF
    beta = INF
    legal_moves = list(game_data.board.legal_moves)

    for move in legal_moves:
        game_data.push_move(move)
        value = min_max(game_data, stats, depth - 1, alpha, beta, False)
        game_data.pop_move()
        stats.inc_nodes_calculated()

        if value > best_value:
            best_move = move
            best_value = value

        alpha = max(alpha, value)

    return best_move


def min_max(game_data, stats, depth, alpha, beta, is_maximizing_player):

    _hash = game_data.zobrist_hash.h()
    stored = tt.get_node(_hash, stats)
    if stored is not None and stored.depth >= depth:
        if stored.kind == "exact":
            stats.inc_hits_exact()
            return stored.value
        elif stored.kind == "alpha":  # upper bound
            stats.inc_hits_alpha()
            beta = min(beta, stored.value)
        elif stored.kind == "beta":  # lower bound
            stats.inc_hits_beta()
            alpha = max(alpha, stored.value)

        if alpha >= beta:
            stats.inc_stored_cut_off()
            return stored.value
        # if stored.depth >= 0: examine stored move first

    legal_moves = list(game_data.board.legal_moves)

    if depth == 0 or len(legal_moves) == 0:
        sign = 1 if game_data.color == chess.WHITE else -1
        return sign * evaluate_position(game_data, stats)

    value = None
    if is_maximizing_player:
        value = -1000000
        current_alpha = alpha  #
        for move in legal_moves:
            game_data.push_move(move)
            value = max(
                value, min_max(game_data, stats, depth - 1, current_alpha, beta, False)
            )
            game_data.pop_move()
            stats.inc_nodes_calculated()

            current_alpha = max(current_alpha, value)  # upper bound
            if value >= beta:
                stats.inc_beta_cut_off()
                break

    else:
        value = +1000000
        current_beta = beta  #
        for move in legal_moves:
            game_data.push_move(move)
            value = min(
                value, min_max(game_data, stats, depth - 1, alpha, current_beta, True)
            )
            game_data.pop_move()
            stats.inc_nodes_calculated()

            current_beta = min(current_beta, value)  # lower bound
            if value <= alpha:
                stats.inc_alpha_cut_off()
                break

    kind = None
    if alpha < value and value < beta:
        kind = "exact"
    elif value <= alpha:  # upper bound
        kind = "alpha"
    elif value >= beta:  # lower bound
        kind = "beta"

    tt.insert_node(_hash, "", value, kind, depth)
    stats.inc_nodes_saved()

    return value