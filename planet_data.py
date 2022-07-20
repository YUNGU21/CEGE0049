# Referenced from: https://github.com/planetlabs/notebooks
# Please install the following package in advance
# pip install requests

# Referenced from: https://developers.planet.com/docs/apis/data/api-mechanics/
import os  # Access environment variables
import requests
import json


# Create a function called 'form' to print the formatted json
def form(content):
    print(json.dumps(content, indent=2))


# Replace your own API key
os.environ['PL_API_KEY'] = 'PLAK84622f71ecea49a09afa4c0cb3cdeaa0'
# Set up your API key from the environment variable
PLANET_API_KEY = os.getenv('PL_API_KEY')
# Set up the base URL
BASE_URL = 'https://api.planet.com/data/v1'
# Set up a session
session = requests.Session()
# Authenticate the session
session.auth = (PLANET_API_KEY, '')
# GET request to the data API
response = session.get(BASE_URL)
if response.status_code == 200:  # Check status
    print('Congratulations! Everything is ready.')
else:
    print('Please check your API Key.')
form(response.json())  # Print response

""" 
Search Stats gives you a quick way to determine the number of items which meets your search specifications. 
Referenced from: https://developers.planet.com/docs/apis/data/search-stats/
                 https://developers.planet.com/docs/apis/data/items-assets/#assets
                 https://developers.planet.com/docs/apis/data/searches-filtering/
# Set up the stats URL
STATS_URL = "{}/stats".format(BASE_URL)
request = {
    "item_types": [
        "PSOrthoTile"
    ],
    "interval": "day",
    "filter": {
       "type": "AndFilter",
       "config": [
           {
              "type": "DateRangeFilter",
              "field_name": "acquired",          # Date-time at which the imagery was captured
              "config": {
                 "gte": "2021-06-08T00:00:00Z",  # Greater than or equal to
                 "lte": "2021-06-09T00:00:00Z"   # Less than or equal to
              }
           },
           {
              "type": "GeometryFilter",
              "field_name": "geometry",
              "config": {
                 "type": "Polygon",
                 "coordinates": [
                    [
                       [
                          9.3485,
                          56.0545
                       ],
                       [
                          10.1635,
                          56.0545
                       ],
                       [
                          10.1635,
                          56.500375
                       ],
                       [
                          9.3485,
                          56.500375
                       ],
                       [
                          9.3485,
                          56.0545
                       ]
                    ]
                 ]
              }
           },
           {
              "type": "RangeFilter",
              "field_name": "cloud_cover",
              "config": {
                 "gte": 0,
                 "lte": 0.01  # cloud cover percentage less than 1%
              }
           },
           {
              "type": "AssetFilter",
              "config": [
                 "analytic_sr"
              ]
           },
           {
              "type": "PermissionFilter",
              "config": [
                 "assets:download"
              ]
           }
       ]
    }
}
# POST request to the stats API
STATS_res = session.post(STATS_URL, json=request)
form(STATS_res.json())  # Print search stats results
"""

"""
Quick search is the easiest way to search the Planet catalog for ad-hoc, everyday use.
# Referenced from: https://developers.planet.com/docs/apis/data/quick-saved-search/
"""
# Set up the quick search URL
QUICK_URL = "{}/quick-search".format(BASE_URL)
request = {
    "item_types": [
        "PSOrthoTile"
    ],
    "filter": {
       "type": "AndFilter",
       "config": [
           {
              "type": "DateRangeFilter",
              "field_name": "acquired",          # Date-time at which the imagery was captured
              "config": {
                 "gte": "2021-05-29T00:00:00Z",  # Greater than or equal to
                 "lte": "2021-05-30T00:00:00Z"   # Less than or equal to
              }
           },
           {
              "type": "GeometryFilter",
              "field_name": "geometry",
              "config": {
                 "type": "Polygon",
                 "coordinates": [
                    [
                       [
                          9.3485,
                          56.0545
                       ],
                       [
                          10.1635,
                          56.0545
                       ],
                       [
                          10.1635,
                          56.500375
                       ],
                       [
                          9.3485,
                          56.500375
                       ],
                       [
                          9.3485,
                          56.0545
                       ]
                    ]
                 ]
              }
           },
           {
              "type": "RangeFilter",
              "field_name": "cloud_cover",
              "config": {
                 "gte": 0,
                 "lte": 0.01  # cloud cover percentage less than 1%
              }
           },
           {
              "type": "AssetFilter",
              "config": [
                 "analytic_sr"
              ]
           },
           {
              "type": "PermissionFilter",
              "config": [
                 "assets:download"
              ]
           }
       ]
    }
}
# POST request to the quick search API
QS_res = session.post(QUICK_URL, json=request, params={"_page_size": 250})  # page size maximum is 250
form(QS_res.json())  # Print quick search results

features = QS_res.json()["features"]
# Count the number
print('The total number of images meet the above requirements is:')
print(len(features))

""""
# Print the detailed information of the first feature
ex = features[0]
form(ex["_permissions"])  # Print the permissions
assets_url = ex["_links"]["assets"]
ex_res = session.get(assets_url)
print(ex_res.json().keys())  # Print the products
"""

# Print the detailed information of each feature with a for loop
ID_list = []
for feature in features:
    print((feature["id"]))  # Print id
    ID_list.append((feature["id"]))
    assets_URL = feature["_links"]["assets"]
    assets_res = session.get(assets_URL)
    sr = assets_res.json()["analytic_sr"]
    form(sr)

    activation_url = sr["_links"]["activate"]
    temp_res = session.get(activation_url)
    form(temp_res.status_code)  # Check status

    # Check active
    asset_active = False
    while asset_active == False:
        active_res = session.get(assets_URL)
        sr_w = active_res.json()["analytic_sr"]
        asset_status = sr_w["status"]
        if asset_status == 'active':
            asset_active = True
            print("Asset is active and ready to download")
    form(sr_w)
    location_url = sr_w["location"]
    print(location_url)

"""
# Set up the order URL
ORDERS_URL = 'https://api.planet.com/compute/ops/orders/v2'
response = session.get(ORDERS_URL)
orders = response.json()['orders']
print(len(orders))
headers = {'content-type': 'application/json'}
request = {
   "name":"order API",
   "products":[
      {
         "item_ids": ID_list,
         "item_type": "PSOrthoTile",
         "product_bundle": "analytic_sr"
      }
   ],
}
def place_order(request):
    response = session.post(ORDERS_URL, data=json.dumps(request), headers=headers)
    print(response)
    order_id = response.json()['id']
    print(order_id)
    order_url = ORDERS_URL + '/' + order_id
    return order_url
order_url = place_order(request)
"""
    
