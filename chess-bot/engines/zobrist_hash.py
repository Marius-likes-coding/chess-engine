import chess

from poly_random_array import POLYGLOT_RANDOM_ARRAY
from pieces import PIECES

SIZE = 781 # 64 * 12 = 768 + 13 (4 + )
NBR_PIECES = 12

def get_all_square_piece_tuples(board):
    square_piece_tuples = []
    
    for i, piece in enumerate(PIECES):
        
        pieces_white = board.pieces(piece, chess.WHITE)
        square_piece_tuples.extend([((2 - chess.WHITE)*i, pw) for pw in pieces_white])
        
        pieces_black = board.pieces(piece, chess.BLACK)
        square_piece_tuples.extend([((2 - chess.BLACK)*i, pb) for pb in pieces_black])
        
    return square_piece_tuples

class ZobristHash:
    def __init__(self):
        self.random_values = POLYGLOT_RANDOM_ARRAY
        

    def from_board(self, board):
        self.zobrist_hash = 0

        for (piece_index, square) in get_all_square_piece_tuples(board):
            self.zobrist_hash ^= POLYGLOT_RANDOM_ARRAY[(64 * piece_index) + square]
        
        return self.zobrist_hash
            
    def to_board(self):
        return None
    
    def make_move(self, move):