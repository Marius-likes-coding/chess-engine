import chess
from time import time

from .evaluate import evaluate_position, MATE
from .game_data import GameData
from .transposition_table import TranspositionTable

INF = 10000000
MIN_DEPTH = 4
MAX_DEPTH = 10

tt = TranspositionTable()


def tt_length():
    return len(tt)


def update_best_moves(parent_best_moves, child_best_moves, current_best_move):
    parent_best_moves.clear()
    parent_best_moves.append(current_best_move)
    parent_best_moves.extend(child_best_moves)


previous_best_moves = []


def is_still_pv_line(current_move, is_pv_line, d):
    if not is_pv_line:
        return False

    global previous_best_moves
    if len(previous_best_moves) <= d:
        return False

    return current_move.uci() == previous_best_moves[d].uci()


def swap_move_to_front(moves_list, d):
    global previous_best_moves
    if len(previous_best_moves) <= d:
        return

    previous_best_move = previous_best_moves[d]
    i = 0
    for move in moves_list:
        if move.uci() == previous_best_move.uci():
            moves_list.pop(i)
            break
        i += 1

    moves_list.insert(0, previous_best_move)


def search_best_move(game_data, stats, max_time=12):
    global previous_best_moves
    previous_best_moves = []
    deadline = time() + max_time

    best_move = None
    current_depth = MIN_DEPTH
    while time() <= deadline and current_depth <= MAX_DEPTH:

        best_moves = []
        move, value = min_max_root(
            game_data, stats, current_depth, deadline, best_moves
        )
        previous_best_moves = best_moves

        if move is None:
            print(f"Search: cancel depth: {current_depth}")
            break

        best_move = move
        print(f"Search: depth {current_depth}, best move {move.uci()}")

        stats.set_depth(current_depth)
        current_depth += 1

        if value == game_data.get_sign() * MATE:
            break

    return best_move


def min_max_root(game_data, stats, depth, deadline, best_moves):
    best_move = None
    best_value = -INF
    alpha = -INF
    beta = INF
    legal_moves = list(game_data.board.legal_moves)
    swap_move_to_front(legal_moves, 0)
    is_pv_line = True

    for move in legal_moves:
        is_pv_line = is_still_pv_line(move, is_pv_line, 0)
        child_best_moves = []
        game_data.push_move(move)
        value = min_max(
            game_data,
            stats,
            depth - 1,
            1,
            alpha,
            beta,
            False,
            depth,
            deadline,
            child_best_moves,
            is_pv_line,
        )
        game_data.pop_move()
        stats.inc_nodes_calculated()

        if value is None or (time() > deadline and depth > MIN_DEPTH):
            return None, None

        if value > best_value:
            best_move = move
            best_value = value
            update_best_moves(best_moves, child_best_moves, best_move)

        alpha = max(alpha, value)

    return best_move, best_value


def min_max(
    game_data,
    stats,
    depth,
    i,
    alpha,
    beta,
    is_maximizing_player,
    current_depth,
    deadline,
    best_moves,
    is_pv_line,
):

    if time() > deadline and current_depth > MIN_DEPTH:
        return None

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
        return game_data.get_sign() * evaluate_position(game_data, stats)

    if is_pv_line:
        swap_move_to_front(legal_moves, i)

    value = None
    best_move = None
    if is_maximizing_player:
        value = -1000000
        current_alpha = alpha  #
        for move in legal_moves:
            is_pv_line = is_still_pv_line(move, is_pv_line, i)
            child_best_moves = []
            game_data.push_move(move)
            new_value = min_max(
                game_data,
                stats,
                depth - 1,
                i + 1,
                current_alpha,
                beta,
                False,
                current_depth,
                deadline,
                child_best_moves,
                is_pv_line,
            )
            game_data.pop_move()
            if new_value is None:
                return None
            if new_value > value:
                value = new_value
                best_move = move
                update_best_moves(best_moves, child_best_moves, best_move)
            stats.inc_nodes_calculated()

            current_alpha = max(current_alpha, value)  # upper bound
            if value >= beta:
                stats.inc_beta_cut_off()
                break

    else:
        value = +1000000
        current_beta = beta  #
        for move in legal_moves:
            is_pv_line = is_still_pv_line(move, is_pv_line, i)
            child_best_moves = []
            game_data.push_move(move)
            new_value = min_max(
                game_data,
                stats,
                depth - 1,
                i + 1,
                alpha,
                current_beta,
                True,
                current_depth,
                deadline,
                child_best_moves,
                is_pv_line,
            )
            game_data.pop_move()
            if new_value is None:
                return None
            if new_value < value:
                value = new_value
                best_move = move
                update_best_moves(best_moves, child_best_moves, best_move)
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