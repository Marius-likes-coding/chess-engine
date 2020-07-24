import json
import chess

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
    "r": {"white": "♜", "black": "♖"},
    "n": {"white": "♞", "black": "♘"},
    "b": {"white": "♝", "black": "♗"},
    "b": {"white": "♛", "black": "♕"},
    "k": {"white": "♚", "black": "♔"},
    "p": {"white": "♟", "black": "♙"},
}


def move_to_unicode(move, game_data):
    board = game_data.board

    source_piece = board.piece_at(move.from_square)
    destin_piece = board.piece_at(move.to_square)

    source_color = color_name(source_piece.color)
    destin_color = color_name(destin_piece.color) if destin_piece else None

    s_piece_uni = UNICODE_PIECE_SYMBOLS[chess.piece_symbol(source_piece)][source_color]
    d_piece_uni = (
        UNICODE_PIECE_SYMBOLS[chess.piece_symbol(destin_piece)][destin_color]
        if destin_piece
        else "empty field"
    )
    return f"{move[:2]} ({s_piece_uni})  → {move[2:]} ({d_piece_uni})"


def color_name(color):
    if color:
        return "white"
    else:
        return "black"


class GameData:
    def __init__(self, game_id):
        self._game_id = game_id
        self._color = None
        self._board = chess.Board()
        self._move_history = []

    @property
    def move_history(self):
        return self._move_history

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def opponent_color(self):
        return color_name(not self._color)


def update_game_data(game_data, event):
    moves = event["moves"]
    if len(moves) == len(game_data.move_history) + 1:
        raw_last_move = moves.split(" ")[-1]
        last_move = chess.Move.from_uci(raw_last_move)

        game_data.board.push(last_move)
        game_data.move_history.append(raw_last_move)

        move_string = move_to_unicode(raw_last_move, game_data)

        print(f"{game_data.opponent_color()} moved: {move_string}")

    else:
        print(
            f"Weird: nbr moves locally: {len(game_data.move_history)}, nbr moves remotely: {len(moves)}"
        )


def make_move(move):
    return 0


def calculate_next_move(game_data):
    return 0


def play(lc_connector, game_id, game_stream):
    game_data = GameData(game_id)

    for raw_event in game_stream:

        if raw_event:
            event = decode_event(raw_event)
            event_type = event["type"]

            if event_type == "gameFull":

                if event[color_name(chess.WHITE)]["id"] == BOT_USERNAME:
                    print(f"Playing as white!")
                    game_data.color = chess.WHITE
                    move = calculate_next_move(game_data)
                    make_move(move)

                elif event[color_name(chess.BLACK)]["id"] == BOT_USERNAME:
                    print(f"Playing as black!")
                    game_data.color = chess.BLACK

                else:
                    print(f"I don't play in this game ? {event}")

            elif event_type == "gameState":
                update_game_data(game_data, event)
                move = calculate_next_move(game_data)
                make_move(move)

            elif event_type == "chatLine":
                print(f"Chat message: {event['username']} >  {event['text']}")

            else:
                print()

        else:
            print(f"[print] ping event: {event}")
