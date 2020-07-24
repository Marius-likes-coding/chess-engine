import requests
import json
import multiprocessing
import random
import backoff

from urllib.parse import urljoin
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout
from urllib3.exceptions import ProtocolError
from http.client import RemoteDisconnected

from pool import LoggingPool
from config.settings import token

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



def watch_event_stream(lc_connector, event_queue):
	response = lc_connector.stream_events()
	
	for event in response.iter_lines():
		if event:
			event_queue.put_nowait(json.loads(event.decode('utf-8')))
		else:
			event_queue.put_nowait({'type': 'ping'})

def play_game(game_id, event_queue):
	print('[print] game started !')
	multiprocessing.get_logger().info('[print] game started !')

if __name__ == '__main__':
	lc_connector = LichessConnector(token)
	event_queue = multiprocessing.Manager().Queue()

	control_stream = multiprocessing.Process(target=watch_event_stream, args=[lc_connector, event_queue])
	control_stream.start()

	with LoggingPool(10) as pool:
		while True:
			event = event_queue.get()

			if event['type'] == 'challenge' and event['challenge']['variant']['key'] == 'standard':
				challenge_id = event['challenge']['id'].strip()
				print('[print] accepting challenge ...')
				lc_connector.accept_challenge(challenge_id)
				print('[print] challenge accepted !')
	
			elif event['type'] == 'gameStart':
				game_id = event['game']['id']
				print('[print] starting game ...')
				pool.apply_async(play_game, [game_id, event_queue])

	control_stream.terminate()
	control_stream.join()