import requests



def get_cheapest_offer(asin):
    token='B9DD68C645191A9DD0E57556'
    url='https://api.zinc.io/v1/products/{}/offers'
    retailer='amazon'

    params = {'retailer':retailer, 'max_age': 30}

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

    # Append the timestamp of the entire request
    min_priced_offer['timestamp'] = timestamp

    return min_priced_offer
