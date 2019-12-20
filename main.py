# import threading
import json
import os
import requests
import shutil
from selenium import webdriver
import sys
import time
from dotenv import load_dotenv

load_dotenv()

terminal_size = shutil.get_terminal_size()
print(terminal_size)


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
auth_url = "https://accounts.spotify.com/authorize"
response_type = "code"
state = "itme"

url = f"{auth_url}?client_id={CLIENT_ID}&response_type={response_type}&redirect_uri={REDIRECT_URI}&state={state}"


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


auth_accept_button = False
timer = 0
while timer < 100 and not auth_accept_button:
    try:
        # auth_accept_button = browser.find_element_by_css_selector("#auth-accept")
        auth_accept_button = browser.find_element_by_id("auth-accept")
    except:
        sys.stdout.write("\nwaiting for auth button")
        sys.stdout.flush()
        time.sleep(0.1)
        timer += 1

auth_accept_button.click()

tok_obj = json.loads(browser.find_element_by_tag_name("pre").text)
res = requests.get(
    "https://api.spotify.com/v1/me",
    headers={"Authorization": f"{tok_obj['token_type']} {tok_obj['access_token']}"},
)
print(res.json())
browser.quit()

while True:
    sys.stdout.write("\r" + time.ctime())
    sys.stdout.write(f"\n your token is: {tok_obj['access_token']}")
    sys.stdout.flush()
    time.sleep(1)
