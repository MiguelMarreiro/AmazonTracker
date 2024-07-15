import requests
import dotenv
from bs4 import BeautifulSoup
import pprint
import os

TARGET_PRICE = 100


def send_bot_message(text):
    parameters_bot = {
        "chat_id": CHAT_ID,
        "text": text,
    }

    response = requests.post(BOT_ENDPOINT, params=parameters_bot)
    response.raise_for_status()


"""Prepares variables and data"""
dotenv.load_dotenv()
url = "https://appbrewery.github.io/instant_pot/"

response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Process the content (for example, print it or parse it with BeautifulSoup)
    content = response.text
    # print(content)
else:
    print(f"Failed to retrieve the URL: {response.status_code}")

soup = BeautifulSoup(content, "html.parser")
# pprint.pp(soup)


"""Scraps price"""
price = float(soup.find(name="span", class_="a-price-whole").text.strip("."))
print(price)

# <span class="a-price-whole">99<span class="a-price-decimal">.</span></span>
"""Send alert"""

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
METHOD = "sendMessage"
BOT_ENDPOINT = f"https://api.telegram.org/bot{BOT_TOKEN}/{METHOD}"

if price < TARGET_PRICE:
    message = f"Price Alert! \nInstant pot price at {price}\n{url}"
    send_bot_message(message)



