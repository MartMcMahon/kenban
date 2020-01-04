# from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import json

# import os
# import shutil
import sys
import requests
import termios
import time
import tty
from auth import Auth
from ui import UI

# Disable line buffering. Thanks stackoverflow
# https://stackoverflow.com/questions/37726138/disable-buffering-of-sys-stdin-in-python-3
tty.setcbreak(sys.stdin.fileno(), termios.TCSANOW)

state = {"mode": "normal", "running": True}
_ui = UI(state)
_auth = Auth(state)


def start():
    eggs = ThreadPoolExecutor()
    listener = eggs.submit(input_listener)
    playing = eggs.submit(get_currently_playing)

    (state["artist"], state["song"]) = playing.result()

    # main loop. quit on 'q'
    while listener.running():
        eggs.submit(_ui.write_frame)
        time.sleep(0.2)
    eggs.shutdown(wait=False)


def input_listener():
    while True:
        ki = sys.stdin.read(1)
        sys.stdin.flush()
        if ki == "i":
            state["mode"] = "insert"
        # elif ki == "h":
        #     _ui.move_cursor(1)
        elif ki == "j":
            _ui.move_selected_line(2)
        elif ki == "k":
            _ui.move_selected_line(3)
        # elif ki == "l":
        #     _ui.move_cursor(4)
        elif ki == "\x1b":
            state["mode"] = "normal"
        elif ki == "q":
            state["running"] = False
            break
        state["last_input"] = ki
        state["needs_update"] = True


def make_api_call():
    pass


def get_currently_playing():
    tok_obj = _auth.creds
    endpoint = "/v1/me/player/currently-playing"
    # r = requests.get(
    #     f"https://api.spotify.com{endpoint}",
    #     headers={"Authorization": f"{tok_obj['token_type']} {tok_obj['access_token']}"},
    # )
    # j = json.loads(r.text)

    # ### read from file for testing
    with open("currently_playing.json", "r") as f:
        j = json.load(f)
    # ### <<

    artist = j["item"]["artists"][0]["name"]
    song = j["item"]["name"]

    state["artist"] = artist
    state["song"] = song

    return (artist, song)


if __name__ == "__main__":
    start()
