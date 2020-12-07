import requests


# def is_final(exception):
#     return isinstance(exception, HTTPError) and exception.response.status_code < 500


class LichessConnector:
    def __init__(self, token):
        self.header = {"Authorization": f"Bearer {token}"}
        self.baseUrl = "https://lichess.org"
        self.session = requests.Session()
        self.session.headers.update(self.header)

    # @backoff.on_exception(backoff.constant,
    #                    (RemoteDisconnected, ConnectionError, ProtocolError, HTTPError, ReadTimeout), max_time=60, interval=0.1, giveup=is_final)
    def get(self, path, stream=False):
        response = self.session.get(f"{self.baseUrl}{path}", timeout=10, stream=stream)
        response.raise_for_status()
        return response

    # @backoff.on_exception(backoff.constant,
    #                    (RemoteDisconnected, ConnectionError, ProtocolError, HTTPError, ReadTimeout), max_time=60, interval=0.1, giveup=is_final)
    def post(self, path, data=None, json=None):
        response = self.session.post(
            f"{self.baseUrl}{path}", data=data, json=json, timeout=10
        )
        response.raise_for_status()
        return response

    # Events

    def stream_events(self):
        return self.get(f"/api/stream/event", stream=True)

    def stream_game(self, game_id):
        return self.get(f"/api/bot/game/stream/{game_id}", stream=True)

    # Challenges

    def create_challenge(self, user_name, rated, clock_limit, clock_increment):
        data = {
            "rated": rated,
            "clock": {"limit": clock_limit, "increment": clock_increment},
        }
        return self.post(f"/api/challenge/{user_name}", json=data)

    def accept_challenge(self, challenge_id):
        return self.post(f"/api/challenge/{challenge_id}/accept").json()

    def decline_challenge(self, challenge_id):
        return self.post(f"/api/challenge/{challenge_id}/decline").json()

    # Games

    def make_move(self, game_id, move):
        return self.post(f"/api/bot/game/{game_id}/move/{move}").json()

    def abort(self, game_id):
        return self.post(f"/api/bot/game/{game_id}/abort").json()

    def resign(self, game_id):
        return self.post(f"/api/bot/game/{game_id}/resign").json()
