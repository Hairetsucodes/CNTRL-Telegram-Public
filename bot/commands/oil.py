


import requests

def oil_price():
    # This is a placeholder URL and API key
    api_url = "https://www.alphavantage.co/query?function=WTI&interval=daily&apikey=UEZCZ77OWPKJHA7J"


    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(api_url, headers=headers)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        # Assuming the API returns a JSON object and the price is stored under 'price'
        oil_price = data
        return oil_price
    else:
        return "Failed to fetch data"

