import requests

url = 'https://api.oilpriceapi.com/v1/prices/latest'
headers = {
  'Authorization': 'Token e7fe08fe4019dab013c50774620aef6f',
  'Content-Type': 'application/json'
}



def oil_price():
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    return data
