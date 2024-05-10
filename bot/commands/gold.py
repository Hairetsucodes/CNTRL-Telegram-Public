import requests

api_url = "https://data-asg.goldprice.org/dbXRates/USD"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
}


def gold_price():
    data = requests.get(api_url, headers=headers).json()
    return data["items"][0]["xauPrice"]
