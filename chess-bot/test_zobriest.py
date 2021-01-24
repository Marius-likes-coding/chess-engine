import random
import chess

from engines.game_data import GameData
from engines.zobrist_hash import ZobristHash

board = [[" " for x in range(8)] for y in range(8)]
piece_list = ["R", "N", "B", "Q", "P"]


def place_kings(brd):
    while True:
        rank_white, file_white, rank_black, file_black = (
            random.randint(0, 7),
            random.randint(0, 7),
            random.randint(0, 7),
            random.randint(0, 7),
        )
        diff_list = [abs(rank_white - rank_black), abs(file_white - file_black)]
        if sum(diff_list) > 2 or set(diff_list) == set([0, 2]):
            brd[rank_white][file_white], brd[rank_black][file_black] = "K", "k"
            break


def populate_board(brd, wp, bp):
    for x in range(2):
        if x == 0:
            piece_amount = wp
            pieces = piece_list
        else:
            piece_amount = bp
            pieces = [s.lower() for s in piece_list]
        while piece_amount != 0:
            piece_rank, piece_file = random.randint(0, 7), random.randint(0, 7)
            piece = random.choice(pieces)
            if (
                brd[piece_rank][piece_file] == " "
                and pawn_on_promotion_square(piece, piece_rank) == False
            ):
                brd[piece_rank][piece_file] = piece
                piece_amount -= 1


def fen_from_board(brd):
    fen = ""
    for x in brd:
        n = 0
        for y in x:
            if y == " ":
                n += 1
            else:
                if n != 0:
                    fen += str(n)
                fen += y
                n = 0
        if n != 0:
            fen += str(n)
        fen += "/" if fen.count("/") < 7 else ""
    fen += " w - - 0 1\n"
    return fen


def pawn_on_promotion_square(pc, pr):
    if pc == "P" and pr == 0:
        return True
    elif pc == "p" and pr == 7:
        return True
    return False


def generate_random_fen():
    piece_amount_white, piece_amount_black = random.randint(0, 15), random.randint(
        0, 15
    )
    place_kings(board)
    populate_board(board, piece_amount_white, piece_amount_black)
    return fen_from_board(board)


fens = [
    ("rnbqkbr1/pppppppp/7n/8/3P4/6P1/PPP1PP1P/RNBQKBNR w KQq - 1 3", "c1e3"),
    "4N3/2p4R/2b1p3/Pp1P1p2/1KPP4/2r2k2/5P2/6b1 w - - 0 1",
    "8/3p1B2/4P1n1/P1b1N3/1P6/PP4p1/Kp1k1p2/4R3 w - - 0 1",
    "2r5/p7/7N/PP2Pp2/8/1pRp3N/3knP2/3b1K2 w - - 0 1",
    "1NR1n3/r1PPbp1P/B1Kp2N1/PPRn2P1/p1PBp1PQ/1ppp2q1/r1b2p2/5k2 w - - 0 1",
    "3B4/2rP1k1K/QPP2r1p/Pp2q2n/bP1p2pp/pPnPbB1N/Pp2p1R1/6NR w - - 0 1",
    "8/2n1rn1P/PNQpN1Pp/1Pp1pP2/1P1BPpq1/4pbR1/KbRPppB1/4kr2 w - - 0 1",
    "3r1q2/1n2P2N/BKp1p1Pp/1p1Rp1Pb/Rb2P3/BPQP1pk1/1ppPPN2/n5r1 w - - 0 1",
    "6nb/2r1PB2/3pppK1/pQPP1P1P/1PpP1R2/2pP1RNp/N4n1p/qr1kB2b w - - 0 1",
    "R2Q4/6Pp/8/3r4/8/3n3k/2K5/8 w - - 0 1",
    "8/4P3/8/1B6/7r/8/3Bpkq1/2K5 w - - 0 1",
    "r6r/1b2k1bq/8/8/7B/8/8/R3K2R b QK - 3 2",
    "8/8/8/2k5/2pP4/8/B7/4K3 b - d3 5 3",
    "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
    "3k4/3p4/8/K1P4r/8/8/8/8 b - - 0 1",
    "8/P1k5/K7/8/8/8/8/8 w - - 0 1",
    "5r1B/bpp5/3R2BP/PP1P1p2/p1PP2nP/P1K5/k2p1Q2/1q2NrR1 w - - 0 1",
    "q5k1/P1PB3p/n3r3/1P1Npn2/1PPb1B2/P2pP1p1/K1P1p3/1Q1Rr3 w - - 0 1",
    "1K6/2P1R3/2Bp4/1PN3pp/Pp1QP2P/k1P4P/nN1pRB2/2bb1q1r w - - 0 1",
    "2BNk3/6P1/P1ppqQ2/nb4Pr/PRp1p2P/1PR5/2p1Pp2/K3B2r w - - 0 1",
    "5b2/1P2k1n1/1QK3p1/3P3R/Npp1n3/pPP4r/1pq1PRpP/2BBN3 w - - 0 1",
    "R5R1/bpB3n1/2PP1P1p/1Npkp3/3p2KP/2P3PN/qp6/1rQ3rn w - - 0 1",
    "3rBb2/P1P3P1/pPq1PPPK/4pN1n/r2pP2B/5k2/1Rb3N1/4Q1n1 w - - 0 1",
    "1B3q2/npp2P2/4Rp2/1P2pP1P/pp1k1P2/1b1PRp2/2pKn1r1/5rN1 w - - 0 1",
    "4B2N/p2Q2P1/1P1BnP2/Pbpp3P/1P4np/b2pNk1p/prp5/6K1 w - - 0 1",
    "r1bqkbnr/ppp1pppp/n2p4/8/8/4P3/PPPP1PPP/RNBQK1NR w KQkq - 0 3",
]

game_data_ = GameData(1)
for fen in fens:
    # if type(fen) is tuple:
    fen1 = "rnbqkbr1/ppppnppp/B3p3/8/4P3/7N/PPPP1PPP/RNBQK2R w KQq - 4 4"
    move = chess.Move.from_uci("e1g1")
    # else:
    # move = random.choice(list(game_data_.board.legal_moves))

    game_data_.board = chess.Board(fen1)
    init_hash = game_data_.zobrist_hash.h()

    push_hash = game_data_.push_move(move)
    fresh_push_hash = ZobristHash().from_board(game_data_.board)

    pop__hash = game_data_.pop_move()
    fresh_pop_hash = ZobristHash().from_board(game_data_.board)

    if (
        init_hash != pop__hash
        or init_hash != fresh_pop_hash
        or push_hash != fresh_push_hash
    ):
        print(f"fen      : {fen1}")
        print(f"move     : {move}")
        print(f"init_hash: {init_hash}\n")
        print(f"push_hash: {push_hash}")
        print(f"fresh_push_hash: {fresh_push_hash}\n")
        print(f"pop__hash: {pop__hash}")
        print(f"fresh_pop_hash: {fresh_pop_hash}")
        break

print("done")
