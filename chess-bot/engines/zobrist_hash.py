import chess

from .poly_random_array import POLYGLOT_RANDOM_ARRAY
from .pieces import PIECES

SIZE = 781  # 64 * 12 = 768 + 13 (4 + 8 + 1)
NBR_PIECES = 12


# def get_all_square_pieces_of_color(board, color):
#     return chess.SquareSet(
#         (
#             board.pawns
#             | board.knights
#             | board.bishops
#             | board.rooks
#             | board.queens
#             | board.kings
#         )
#         & board.occupied_co[color]
#     )


def get_piece_index(piece, color, square):
    # print(f"piece {piece}, color {color}, square {square}")
    piece_index = (2 - color) * (piece - 1)
    return (64 * piece_index) + square


def get_all_piece_indexes(board):
    square_piece_tuples = []

    for piece in range(1, 7):

        pieces_white = board.pieces(piece, chess.WHITE)
        for white_square in pieces_white:
            square_piece_tuples.append(
                get_piece_index(piece, chess.WHITE, white_square)
            )

        pieces_black = board.pieces(piece, chess.BLACK)
        for black_square in pieces_black:
            square_piece_tuples.append(
                get_piece_index(piece, chess.BLACK, black_square)
            )

    return square_piece_tuples


class ZobristHash:
    def __init__(self):
        self.zobrist_hash = 0
        self.castling_rights = [True, True, True, True]

    def h(self):
        return self.zobrist_hash

    def calculate_from_scratch(self, board):
        self.zobrist_hash = 0

        # Hash in the pieces [0 ... 767].
        for piece_index in get_all_piece_indexes(board):
            self.zobrist_hash ^= POLYGLOT_RANDOM_ARRAY[piece_index]

        # Hash in the special flags
        self.castling_rights = self.get_current_castling_rights(board)
        self.apply_special_flags(board, self.castling_rights)

        return self.zobrist_hash

    def from_board(self, board):
        return self.calculate_from_scratch(board)

    def get_special_flags(self, board, castling_rights):
        special_flags = 0

        # Hash in the castling flags [768 ... 771].
        if castling_rights[0]:  # white_king
            special_flags ^= POLYGLOT_RANDOM_ARRAY[768]
        if castling_rights[1]:  # white_queen
            special_flags ^= POLYGLOT_RANDOM_ARRAY[769]
        if castling_rights[2]:  # black_king
            special_flags ^= POLYGLOT_RANDOM_ARRAY[770]
        if castling_rights[3]:  # black_queen
            special_flags ^= POLYGLOT_RANDOM_ARRAY[771]

        # Hash in the en passant file [772 ... 779].
        if board.ep_square:
            # But only if there's actually a pawn ready to capture it. Legality
            # of the potential capture is irrelevant.
            if board.turn == chess.WHITE:
                ep_mask = chess.shift_down(chess.BB_SQUARES[board.ep_square])
            else:
                ep_mask = chess.shift_up(chess.BB_SQUARES[board.ep_square])

            ep_mask = chess.shift_left(ep_mask) | chess.shift_right(ep_mask)

            if ep_mask & board.pawns & board.occupied_co[board.turn]:
                rand = POLYGLOT_RANDOM_ARRAY[772 + chess.square_file(board.ep_square)]
                special_flags ^= rand

        # Hash in turn [780]
        if board.turn == chess.WHITE:
            special_flags ^= POLYGLOT_RANDOM_ARRAY[780]

        return special_flags

    def apply_special_flags(self, board, castling_rights):
        self.special_flags = self.get_special_flags(board, castling_rights)
        self.zobrist_hash ^= self.special_flags

    def remove_special_flags(self):
        self.zobrist_hash ^= self.special_flags
        self.special_flags = 0

    def get_current_castling_rights(self, board):
        white_king = board.has_kingside_castling_rights(chess.WHITE)
        white_queen = board.has_queenside_castling_rights(chess.WHITE)
        black_king = board.has_kingside_castling_rights(chess.BLACK)
        black_queen = board.has_queenside_castling_rights(chess.BLACK)
        return [white_king, white_queen, black_king, black_queen]

    def castling_rights_arrays_different(self, other):
        return (
            other[0] != self.castling_rights[0]
            or other[1] != self.castling_rights[1]
            or other[2] != self.castling_rights[2]
            or other[3] != self.castling_rights[3]
        )

    def make_move(self, board, move, dropped_piece=None):

        current_castling_rights = self.get_current_castling_rights(board)

        if self.castling_rights_arrays_different(current_castling_rights):
            return self.calculate_from_scratch(board)

        # Hash out the special flags
        self.remove_special_flags()

        from_piece = (
            chess.PAWN
            if move.promotion is not None
            else board.piece_type_at(move.to_square)
        )
        from_color = board.color_at(move.to_square)
        from_index = get_piece_index(from_piece, from_color, move.from_square)

        # Hash out the piece at its FROM square
        self.zobrist_hash ^= POLYGLOT_RANDOM_ARRAY[from_index]

        # If a piece was dropped, hash it out of the TO square
        if dropped_piece is not None:
            drop_piece = dropped_piece
            drop_color = not from_color
            drop_index = get_piece_index(drop_piece, drop_color, move.to_square)

            self.zobrist_hash ^= POLYGLOT_RANDOM_ARRAY[drop_index]

        to_piece = board.piece_type_at(move.to_square)
        to_index = get_piece_index(to_piece, from_color, move.to_square)

        # Hash in the piece at its TO square
        self.zobrist_hash ^= POLYGLOT_RANDOM_ARRAY[to_index]

        # Hash in the special flags
        self.apply_special_flags(board, self.castling_rights)
        return self.zobrist_hash

    def undo_move(self, board, move):

        current_castling_rights = self.get_current_castling_rights(board)

        if self.castling_rights_arrays_different(current_castling_rights):
            return self.calculate_from_scratch(board)

        # Hash out the special flags
        self.remove_special_flags()

        to_piece = (
            move.promotion
            if move.promotion is not None
            else board.piece_type_at(move.from_square)
        )
        to_color = board.color_at(move.from_square)
        # print(f"to_piece: {to_piece}")
        # print(f"to_color: {to_color}")
        # print(f"to_square: {move.to_square}")
        to_index = get_piece_index(to_piece, to_color, move.to_square)

        # Hash out the piece at its TO square
        self.zobrist_hash ^= POLYGLOT_RANDOM_ARRAY[to_index]

        from_piece = board.piece_type_at(move.from_square)
        # print(f"from_piece: {from_piece}")
        # print(f"from_color: {to_color}")
        # print(f"from_square: {move.from_square}")
        from_index = get_piece_index(from_piece, to_color, move.from_square)

        # Hash in the piece at its FROM square
        self.zobrist_hash ^= POLYGLOT_RANDOM_ARRAY[from_index]

        # If a piece was dropped, hash it in the TO square
        drop_piece = board.piece_type_at(move.to_square)
        if drop_piece is not None:
            drop_color = not to_color
            # print(f"drop_piece: {drop_piece}")
            # print(f"drop_color: {drop_color}")
            # print(f"drop_square: {move.to_square}")
            drop_index = get_piece_index(drop_piece, drop_color, move.to_square)

            self.zobrist_hash ^= POLYGLOT_RANDOM_ARRAY[drop_index]

        # Hash in the special flags
        self.apply_special_flags(board, self.castling_rights)
        return self.zobrist_hash
