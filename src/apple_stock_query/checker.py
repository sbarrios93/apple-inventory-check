import json
import requests
from pushsafer import Client
from dotenv import load_dotenv
import os

try:
    load_dotenv()
except:
    pass


PUSH_DEVICE = os.getenv("72663")

SEARCH_STORES = ["R076", "R149", "R021", "R346", "R110"]

MODELS = {
    "iPhone 15 Pro Max 256GB Natural Titanium": "MU683LL/A",
    "iPhone 15 Pro Max 512GB Natural Titanium": "MU63LL/A",
    "iPhone 15 Blue": "MTM73LL/A"
}


ZIPCODE = "02445"

URL = "https://www.apple.com/shop/fulfillment-messages?store={}&parts.0={}&cppart=UNLOCKED/US&purchaseOption=fullPrice"


client = Client(os.getenv("PUSH_KEY"))


def checker() -> None:

    for model, sku in MODELS.items():
        for combination_lookup in zip(SEARCH_STORES, [sku] * len(SEARCH_STORES)):
            response = requests.get(URL.format(*combination_lookup))
            data = json.loads(response.text)
            state = data["body"]["content"]["pickupMessage"]["stores"][0][
                "partsAvailability"
            ][sku]["pickupDisplay"]

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
