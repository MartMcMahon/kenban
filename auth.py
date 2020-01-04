import json
import os
import requests
from selenium import webdriver
import sys
import time
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
auth_url = "https://accounts.spotify.com/authorize"
response_type = "code"
scopes = "user-modify-playback-state user-read-playback-state"
state = "itme"

url = f"{auth_url}?client_id={CLIENT_ID}&response_type={response_type}&redirect_uri={REDIRECT_URI}&state={state}&scope={scopes}"


class Auth:
    def __init__(self, state):
        self.creds = self.load_creds()

    def load_creds(self):
        with open("creds.json", "r") as f:
            return json.load(f)

    def save_creds(self):
        options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(executable_path="./chromedriver", options=options)
        browser.get(url)

        user_input = browser.find_element_by_id("login-username")
        user_input.clear()
        user_input.send_keys(USERNAME)
        password_input = browser.find_element_by_id("login-password")
        password_input.clear()
        password_input.send_keys(PASSWORD)
        login_button = browser.find_element_by_id("login-button")
        login_button.click()

        time.sleep(1)
        tok_obj = json.loads(browser.find_element_by_tag_name("body").text)
        res = requests.get(
            "https://api.spotify.com/v1/me",
            headers={
                "Authorization": f"{tok_obj['token_type']} {tok_obj['access_token']}"
            },
        )
        browser.quit()

        with open("creds.json", "w") as f:
            f.write(json.dumps(tok_obj))


# auth button disapeared?
# auth_accept_button = False
# timer = 0
# while timer < 100 and not auth_accept_button:
#     try:
#         # auth_accept_button = browser.find_element_by_css_selector("#auth-accept")
#         auth_accept_button = browser.find_element_by_id("auth-accept")
#         break
#     except:
#         sys.stdout.write("\nwaiting for auth button")
#         sys.stdout.flush()
#         time.sleep(0.1)
#         timer += 1

# if auth_accept_button:
#     auth_accept_button.click()
