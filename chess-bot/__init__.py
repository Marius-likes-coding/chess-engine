import requests
import json
import multiprocessing
import random

from urllib.parse import urljoin
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout
from urllib3.exceptions import ProtocolError
from http.client import RemoteDisconnected

from config.settings import token, url

class LichessConnector():

    def __init__(self, token):
        self.header = {'Authorization': f'Bearer {token}'}
        self.baseUrl = "https://lichess.org"
        self.session = requests.Session()
        self.session.headers.update(self.header)

    @backoff.on_exception(backoff.constant, 
        (RemoteDisconnected, ConnectionError, ProtocolError, HTTPError, ReadTimeout), max_time=60, interval=0.1, giveup=is_final)
    def get(self, path, stream=False):
        response = self.session.get(f"{self.baseUrl}{path}", timeout=2, stream=stream)
        response.raise_for_status()
        return response

    @backoff.on_exception(backoff.constant, 
        (RemoteDisconnected, ConnectionError, ProtocolError, HTTPError, ReadTimeout), max_time=60, interval=0.1, giveup=is_final)
    def post(self, path, data=None):
        response = self.session.post(f"{self.baseUrl}{path}", data=data, timeout=2)
        response.raise_for_status()
        return response
    
    # Events

    def stream_events(self):
        return self.get(f"/api/stream/event", stream=True)
    
    # Challenges

    def accept_challenge(self, challenge_id):
        return self.post(f"/api/challenge/{challenge_id}/accept").json()

    def decline_challenge(self, challenge_id):
        return self.post(f"/api/challenge/{challenge_id}/decline").json()
    
    # Games

    def stream_game(self, game_id):
        return self.get(f"/api/bot/game/stream/{game_id}", stream=True)

    def make_move(self, game_id, move):
        return self.post(f"/api/bot/game/{game_id}/move/{move}").json()

    def abort(self, game_id):
        return self.post(f"/api/bot/game/{game_id}/abort").json()

    def resign(self, game_id):
        return self.post(f"/api/bot/game/{game_id}/resign").json()



def stream_events(event_queue):
	response = requests.get(url + 'api/stream/event', headers=headers, stream=True)
	
	for event in response.iter_lines():
		if event:
			event_queue.put_nowait(json.loads(event.decode('utf-8')))
		else:
			event_queue.put_nowait({'type': 'ping'})

def play_game(game_id, event_queue):
	start_color = 1
	my_time = 'btime'
	game_stream = game_updates(game_id).iter_lines()

	print('GAME_STREAM')
	print(game_stream)

	game = json.loads(next(game_stream).decode('utf-8'))
	variant = game['variant']['key']

	in_book = True
	current_book = None

	if variant == 'atomic':
		board = chess.variant.AtomicBoard()
	if variant == 'antichess':
		board = chess.variant.GiveawayBoard()
	if variant == 'standard':
		current_book = standard_book
		print("Choosing book standard_book")
		board = chess.Board()

	fens = []

	if game['white']['id'] == BOT_ID:
		start_color = -1
		my_time = 'wtime'

		if variant == 'atomic':
			print("Choosing book atomic_white")
			current_book = atomic_white

		#bot_move = search(board, color=-start_color, variant=variant, depth=3)

		if current_book:
			book_move = current_book.get_moves([])
		if variant == 'antichess':
			bot_move = random.choice(['e2e3', 'b2b3', 'g2g3'])
		else:
			bot_move = random.choice(book_move)

		make_move(game_id, bot_move)
		fens.append(board.fen()[:-9].strip())
	elif game['black']['id'] == BOT_ID and variant == 'atomic':
		print("Choosing book atomic_black")
		current_book = atomic_black

	for event in game_stream:
		upd = json.loads(event.decode('utf-8')) if event else None
		_type = upd['type'] if upd else 'ping'
		if (_type == 'gameState'):
			last_move = upd['moves'].split(' ')[-1]
			last_move = chess.Move.from_uci(last_move)
			board.push(last_move)

			moves = upd['moves'].split(' ')

			if (in_book and current_book):
				book_move = current_book.get_moves(moves)
			else:
				book_move = None

			if in_book and not book_move:
				print(in_book)
				chat(game_id, "I'm out of book! :O")
				print("Out of book!")
				in_book = False

			if book_move:
				print("Book moves:")
				print(book_move)
				bot_move = random.choice(book_move)
				bot_move = chess.Move.from_uci(bot_move)
			else:
				bot_move = search(board, color=-start_color, variant=variant, depth=time_to_depth(upd[my_time], variant))

			print(bot_move)

			make_move(game_id, bot_move)
			fens.append(board.fen()[:-9].strip())

if __name__ == '__main__':
	event_queue = multiprocessing.Manager().Queue()

	control_stream = multiprocessing.Process(target=stream_events, args=[event_queue])
	control_stream.start()

	with logging_pool.LoggingPool(10) as pool:
		while True:
			event = event_queue.get()

			if event['type'] == 'challenge' and ((event['challenge']['variant']['key'] == 'standard') or (event['challenge']['variant']['key'] == 'atomic') or (event['challenge']['variant']['key'] == 'antichess')):
				_id = event['challenge']['id'].strip()

				accept_challenge(_id)
			elif event['type'] == 'gameStart':
				game_id = event['game']['id']
				pool.apply_async(play_game, [game_id, event_queue])

	control_stream.terminate()
	control_stream.join()