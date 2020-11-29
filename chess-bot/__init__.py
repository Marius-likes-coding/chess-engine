import json
import multiprocessing
import random
import backoff
import requests
import time
import traceback

from urllib.parse import urljoin
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout
from urllib3.exceptions import ProtocolError
from http.client import RemoteDisconnected
from bs4 import BeautifulSoup
from random import shuffle

from lichess import LichessConnector
from engines.trivial import play
from config.settings import token, bot_username
from pool import LoggingPool


def watch_event_stream(lc_connector, event_queue):
    response = lc_connector.stream_events()
    print(response.status_code)
    print(response.url)

    for event in response.iter_lines():
        if event:
            event_queue.put_nowait(json.loads(event.decode("utf-8")))
        else:
            event_queue.put_nowait({"type": "ping"})


def scrape_online_bots():
    response = requests.get("https://lichess.org/player/bots")
    soupPage = BeautifulSoup(response.content, "html.parser")

    bot_names = []
    for a in soupPage.find_all("a", {"class": "online user-link ulpt"}):
        bot_names.append(a["href"][3:])
    return bot_names


def create_challenge(lc_connector, user_name):
    response = lc_connector.create_challenge(
        user_name, rated=True, clock_limit=300, clock_increment=0
    )
    print(f"[print] Challenged {user_name}: {response.status_code}")


def challenge_online_bots(lc_connector):
    bot_names = scrape_online_bots()
    shuffle(bot_names)
    print(f"[print] {len(bot_names)} bots online")
    for bot_name in bot_names:
        create_challenge(lc_connector, bot_name)
        time.sleep(60)


def play_game(lc_connector, game_id):
    print("[print] game started !")
    multiprocessing.get_logger().debug("[print] game started !")

    game_stream = lc_connector.stream_game(game_id).iter_lines()
    try:
        play(lc_connector, game_id, game_stream)
    except Exception as e:
        print("E:", e)
        print(traceback.print_exc())
        print(traceback.format_exc())


if __name__ == "__main__":
    print("Starting ...")
    lc_connector = LichessConnector(token)
    event_queue = multiprocessing.Manager().Queue()

    print("spawning event stream watch ...")
    control_stream = multiprocessing.Process(
        target=watch_event_stream, args=[lc_connector, event_queue]
    )
    control_stream.start()
    multiprocessing.get_logger().debug("[logger] event stream watch spawned !")
    print("event stream watch spawned !")

    # challenge_online_bots(lc_connector)

    with LoggingPool(10) as pool:
        while True:
            event = event_queue.get()

            if (
                event["type"] == "challenge"
                and event["challenge"]["variant"]["key"] == "standard"
                and event["challenge"]["challenger"]["name"] != bot_username
                and event["challenge"]["timeControl"]["limit"] >= 600
            ):
                challenge_id = event["challenge"]["id"].strip()
                print("[print] accepting challenge ...")
                lc_connector.accept_challenge(challenge_id)
                print("[print] challenge accepted !")

            elif event["type"] == "gameStart":
                game_id = event["game"]["id"]
                print(f"[print] starting game {game_id} ...")
                print(f"Link: https://lichess.org/{game_id}")
                pool.apply_async(play_game, [lc_connector, game_id])

            # else:
            # print(f"[print] Event: {event}")

    control_stream.terminate()
    control_stream.join()
