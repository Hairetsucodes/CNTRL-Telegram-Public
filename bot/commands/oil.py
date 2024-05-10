


import requests

def oil_price():
    # This is a placeholder URL and API key
    api_url = "https://api.oilpriceapi.com/v1/prices/latest"
    api_key = "UEZCZ77OWPKJHA7J"

    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Assuming the API returns a JSON object and the price is stored under 'price'
        oil_price = data['data']['price']
        return oil_price
    else:
        return "Failed to fetch data"

