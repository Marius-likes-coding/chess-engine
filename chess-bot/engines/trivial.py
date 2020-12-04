import json
import random
import chess
import time

from .minmax import min_max_first_iteration
from .minmax_a_b_proning import a_b_min_max_first_iteration
from .minmax_ab_tt import search_move, tt_length
from .game_data import GameData
from .search_stats import SearchStats

BOT_USERNAME = "Chestor2008"


def decode_event(event):
    return json.loads(event.decode("utf-8"))


# PIECE_TYPES   = [      PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
# PIECE_SYMBOLS = [None, "p",  "n",    "b",    "r",  "q",   "k"]


# def piece_symbol(piece_type):
#     return PIECE_SYMBOLS[piece_type]

# def piece_symbol_unicode(piece_type, color):
#     return UNICODE_PIECE_SYMBOLS[piece_type][color]

UNICODE_PIECE_SYMBOLS = {
    "♜": "black",
    "♞": "black",
    "♝": "black",
    "♛": "black",
    "♚": "black",
    "♟": "black",
    "♖": "white",
    "♘": "white",
    "♗": "white",
    "♕": "white",
    "♔": "white",
    "♙": "white",
}


def move_to_unicode(move, raw_move, game_data):
    board = game_data.board

    source_piece = board.piece_at(move.from_square)
    destin_piece = board.piece_at(move.to_square)

    # source_color = color_name(source_piece.color) if source_piece else None
    # destin_color = color_name(destin_piece.color) if destin_piece else None

    s_piece_uni = source_piece.unicode_symbol() if source_piece else "empty field"
    d_piece_uni = destin_piece.unicode_symbol() if destin_piece else "empty field"

    return (
        f"{raw_move[:2]} ({s_piece_uni})  → {raw_move[2:]} ({d_piece_uni})",
        s_piece_uni,
    )


def color_name(color):
    if color:
        return "white"
    else:
        return "black"


def parse_and_save_move(game_data, raw_move):
    move = chess.Move.from_uci(raw_move)
    game_data.board.push(move)
    game_data.move_history.append(raw_move)
    return move


def update_game_data(game_data, event):
    moves = event["moves"].split(" ")

    local_nbr_moves = len(game_data.move_history)
    remote_nbr_moves = len(moves)

    if len(moves) > len(game_data.move_history) + 1:
        print(
            f"Catching up on moves: nbr moves locally: {local_nbr_moves}, nbr moves remotely: {remote_nbr_moves} -> remote moves: {moves}"
        )

    moves_to_catch_up = remote_nbr_moves - local_nbr_moves

    if moves_to_catch_up > 0 and moves[0] != "":
        for raw_move in moves[
            remote_nbr_moves - moves_to_catch_up : remote_nbr_moves - 1
        ]:
            parse_and_save_move(game_data, raw_move)

        move = chess.Move.from_uci(moves[-1])
        move_string, source_piece_uni = move_to_unicode(move, moves[-1], game_data)

        game_data.board.push(move)
        game_data.move_history.append(moves[-1])

        # announce last move
        color_last_move = UNICODE_PIECE_SYMBOLS[source_piece_uni]
        print(f"{color_last_move} moved: {move_string}")


def check_if_my_turn(game_data):
    if len(game_data.move_history) % 2 == 0:
        # white's turn
        if game_data.color == chess.WHITE:
            return True
    else:
        # black's turn
        if game_data.color == chess.BLACK:
            return True

    return False


def make_move(lc_connector, game_data, move):
    lc_connector.make_move(game_data.game_id, move.uci())


def calculate_next_move(game_data):
    start_time = time.time()
    # random_move = next(iter(game_data.board.legal_moves))
    stats = SearchStats()
    best_move = search_move(game_data, stats)
    # best_move = a_b_min_max_first_iteration(game_data, 4, True)
    print("Move calculation time: %s seconds " % (time.time() - start_time))
    print(stats)
    print(f"TT size: {tt_length()}")
    return best_move


def play(lc_connector, game_id, game_stream):
    game_data = GameData(game_id)

    for raw_event in game_stream:

        if raw_event:
            event = decode_event(raw_event)
            event_type = event["type"]

            if event_type == "gameFull":

                status = event["state"]["status"]
                if status != "started":
                    print(f"Status: {status}")
                print(event)
                if event[color_name(chess.WHITE)].get("name") == BOT_USERNAME:
                    print(f"Playing as white!")
                    game_data.color = chess.WHITE

                elif event[color_name(chess.BLACK)].get("name") == BOT_USERNAME:
                    print(f"Playing as black!")
                    game_data.color = chess.BLACK

                else:
                    print(f"I don't play in this game ? {event}")

                update_game_data(game_data, event["state"])
                is_my_turn = check_if_my_turn(game_data)
                if is_my_turn:
                    move = calculate_next_move(game_data)
                    make_move(lc_connector, game_data, move)

            elif event_type == "gameState":
                status = event["status"]
                if status != "started":
                    print(f"Status: {status}")
                    continue
                update_game_data(game_data, event)
                is_my_turn = check_if_my_turn(game_data)
                if is_my_turn:
                    move = calculate_next_move(game_data)
                    make_move(lc_connector, game_data, move)

            elif event_type == "chatLine":
                print(f"Chat message: {event['username']} >  {event['text']}")

            else:
                print()

        # else:
        # print(f"[print] ping event: {raw_event}")
