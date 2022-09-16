# Referenced from: https://github.com/planetlabs/notebooks
# Please install the following package in advance
# pip install requests

# Referenced from: https://developers.planet.com/docs/apis/data/api-mechanics/
import os  # Access environment variables
import requests
import json
import time

# Create a function called 'form' to print the formatted json
def form(content):
    print(json.dumps(content, indent=2))


# Replace your own API key
os.environ['PL_API_KEY'] = 'PLAK4d2f2314a4104589a16763285dc10699'
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

# Set up the quick search URL
QUICK_URL = '{}/quick-search'.format(BASE_URL)
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
                           9.350520597536402,
                           56.05208492062207
                       ],
                       [
                           10.15317787370242,
                           56.04719487074356
                       ],
                       [
                           10.166771236620633,
                           56.49632920733372
                       ],
                       [
                           9.354653474719425,
                           56.50130250198456
                       ],
                       [
                           9.350520597536402,
                           56.05208492062207
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
           }
       ]
    }
}

# POST request to the quick search API
QS_res = session.post(QUICK_URL, json=request, params={'_page_size': 250})  # page size maximum is 250
print('Searching for images within the filters')
# form(QS_res.json())  # Print quick search results

# Count the number
features = QS_res.json()['features']
print('The total number of images meet the above requirements is:')
print(len(features))

# Get the detailed information of each feature with a for loop
ID_list = []
for feature in features:
    # print((feature['id']))  # Print id
    ID_list.append((feature['id']))

links_dict = {}
status_dict = {}

for idx in ID_list:
    url = 'https://api.planet.com/data/v1/item-types/{}/items/{}/assets'
    idx_url = url.format('PSOrthoTile', idx)
    res = requests.get(idx_url, auth=(PLANET_API_KEY, ''))
    # form(res.json())
    if res.status_code == 429:  # Check the rate limiting error
        raise Exception('Rate Limiting error')
    # Product types: "analytic", "analytic_5b", "analytic_5b_xml", "analytic_dn", "analytic_dn_xml", "analytic_sr", "analytic_xml", "udm", "udm2", "visual", "visual_xml"
    # print(res.json().keys())

    permissions = res.json()['analytic_sr']['_permissions']
    links = res.json()['analytic_sr']['_links']
    self_link = links['_self']
    activate_link = links['activate']
    status = res.json()['analytic_sr']['status']
    print(idx, ':', status)

    if 'download' in permissions:
        status_dict.update({idx: status})
        links_dict.update({idx: (self_link, activate_link)})
        if status != 'active':
            activate_res = requests.get(activate_link, auth=(PLANET_API_KEY, ''))
    else:
        print('Sorry, you can not download this product.')
        continue

download_dict = {}
while ('inactive' in status_dict.values()) or 'activating' in status_dict.values():
    print('Please wait for another one minute to check again.')
    time.sleep(60)
    print('Current status:')
    print(status_dict)

    for idx, link in links_dict.items():
        self_link = link[0]
        activate_status = requests.get(self_link, auth=(PLANET_API_KEY, ''))

        status = activate_status.json()['status']
        status_dict[idx] = status
        print(idx, ':', status)
        activate_link = link[1]

        if (status != 'active') and (status != 'activating'):
            print('This product has not been activated.')
            activate_res = requests.get(activate_link, auth=(PLANET_API_KEY, ''))  # Activate again
            if res.status_code == 429:  # Check the rate limiting error
                raise Exception('Rate Limiting error')

for idx, link in links_dict.items():
    self_link = links_dict[idx][0]
    activation_status = requests.get(self_link, auth=(PLANET_API_KEY, ''))
    status = activation_status.json()['status']
    if status == 'active':
        download_link = activation_status.json()["location"]
        os.system('curl -L ' + str(download_link) + ' > E:\\planetapi\\' + str(idx) + '_analytic_sr.tif \n')
        download_dict.update({idx: activation_status.json()['location']})

# Save all the download links in one csv file
with open('DownloadLinks.csv', 'w+') as output:
    for key, value in download_dict.items():
        output.write(str(key) + ',' + str(value) + '\n')
