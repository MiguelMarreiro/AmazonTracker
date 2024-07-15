import requests
import dotenv
from bs4 import BeautifulSoup
import pprint
import os



def add_tracked_products():
    with open("tracked_products.csv", "a") as file:
        is_continue = True
        new_products = []
        while is_continue:
            print("Input EXIT to quit")
            name = input("Input product's name: ")
            url = input("Input product's url: ")
            price = input("Input product's price: ")

            if url == "EXIT" or name == "EXIT" or price == "EXIT":
                is_continue = False
            else:
                new_products.append(f"{name},{url}")
        file.writelines(new_products)


def send_bot_message(text):
    parameters_bot = {
        "chat_id": CHAT_ID,
        "text": text,
    }

    response = requests.post(BOT_ENDPOINT, params=parameters_bot)
    response.raise_for_status()

"""Add products"""
add_tracked_products()
"""Prepares variables and data"""
dotenv.load_dotenv()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,pt-PT;q=0.8,pt;q=0.7",
    "Dnt": "1",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

with open("tracked_products.csv", "r") as file:
    database = file.readlines()
    print(database)

for product in database:
    name = product.split(",")[0]
    url = product.split(",")[1]
    target_price = float(product.split(",")[2])

    response = requests.get(url=url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the content (for example, print it or parse it with BeautifulSoup)
        content = response.text
        # print(content)
    else:
        print(f"Failed to retrieve the URL: {response.status_code}")

    soup = BeautifulSoup(content, "html.parser")
    pprint.pp(soup)


    """Scraps price"""
    price = float(soup.find(name="span", class_="a-price-whole").text)
    print(price)

    # <span class="a-price-whole">99<span class="a-price-decimal">.</span></span>
    """Send alert"""

    BOT_TOKEN = os.environ["BOT_TOKEN"]
    CHAT_ID = os.environ["CHAT_ID"]
    METHOD = "sendMessage"
    BOT_ENDPOINT = f"https://api.telegram.org/bot{BOT_TOKEN}/{METHOD}"

    if price < target_price:
        message = f"Price Alert! \nInstant pot price at {price}\n{url}"
        send_bot_message(message)
    #
    #
    #
