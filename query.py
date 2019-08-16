import requests

token='B9DD68C645191A9DD0E57556'
url='https://api.zinc.io/v1/products/{}/offers'
retailer='amazon'

params = {'retailer':retailer}

asin='B07V4MN4GD'

r = requests.get(url = url.format(asin), params = params, auth = (token,''))

print(str(r))

data = r.json()

print(data)

asin = data['asin']
retailer = data['retailer']
timestamp = data['timestamp']

print(timestamp)
print(asin)
print(retailer)

# We only care about the cheapest order
min_priced_offer = min(data['offers'], key=lambda x:x['price'])

offer_id = min_priced_offer['offer_id']
seller_id = min_priced_offer['seller']['id']
seller_name = min_priced_offer['seller']['name']
price = min_priced_offer['price']
currency = min_priced_offer['currency']

print(offer_id)
print(seller_id)
print(seller_name)
print(price)
print(currency)
