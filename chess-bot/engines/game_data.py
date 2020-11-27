import chess


class GameData:
    def __init__(self, game_id):
        self._game_id = game_id
        self._color = None
        self._board = chess.Board()
        self._move_history = []

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board

    @property
    def game_id(self):
        return self._game_id

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
        return not self._color
