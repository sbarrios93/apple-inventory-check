import json
import requests
from pushsafer import Client
from dotenv import load_dotenv
import os

try:
    load_dotenv()
except:
    pass


PUSH_DEVICE = 72663

SEARCH_STORES = ["R076", "R149", "R021", "R346", "R110"]

MODELS = {
    "iPhone 15 Pro Max 256GB Natural Titanium": "MU683LL/A",
    "iPhone 15 Pro Max 512GB Natural Titanium": "MU6D3LL/A",
    "iPhone 15 Pro Max 256GB Blue Titanium": "MU693LL/A",
    "iPhone 15 Pro Max 512GB Blue Titanium": "MU6E3LL/A",
}


URL = "https://www.apple.com/shop/fulfillment-messages?store={}&parts.0={}&cppart=UNLOCKED/US&purchaseOption=fullPrice"


client = Client(os.environ["PUSHSAFER_PRIVATE_KEY"])


def checker() -> None:

    for model, sku in MODELS.items():
        for combination_lookup in zip(SEARCH_STORES, [sku] * len(SEARCH_STORES)):
            response = requests.get(URL.format(*combination_lookup))
            data = json.loads(response.text)
            try:
                state = data["body"]["content"]["pickupMessage"]["stores"][0][
                "partsAvailability"
            ][sku]["pickupDisplay"]
            except KeyError:
                print(f"{model} not available in {URL.format(*combination_lookup)})")
                continue

            if state == "available":
                store_name = data["body"]["content"]["pickupMessage"]["stores"][0][
                    "storeName"]
                client.send_message(
                    f"https://www.apple.com/shop/buy-iphone/iphone-15-pro/6.7-inch-display-256gb-natural-titanium-t-mobile",
                    f"{model} available in {store_name}!",
                    device=PUSH_DEVICE,
                )
            else:
                print(f"{model} not available in {combination_lookup[0]}")
