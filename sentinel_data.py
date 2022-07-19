# Download customized Sentinel-2 satellite images
# Referenced from: https://github.com/sentinelsat/sentinelsat

# Please install the following package 'sentinelsat' in advance
# pip install sentinelsat

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

# Connect to your API with necessary account information
# api = SentinelAPI('Username', 'Password', 'link')
# link 1: Open Hub
api = SentinelAPI('spady', 'woshizhangyu', 'https://scihub.copernicus.eu/dhus')
# link 2: API Hub
# api = SentinelAPI('spady', 'woshizhangyu', 'https://apihub.copernicus.eu/apihub')

# Search by polygon, time, and Hub query keywords e.g. product type, cloud cover percentage
# Set your area of interest
# Creating Geometry: http://geojson.io/#map=2/20.0/0.0
AOI = geojson_to_wkt(read_geojson('studyarea.geojson'))
# Set your searching period with the start and end date as 'YYYYMMDD'
START = '20210101'
END = '20211231'
# Set your specific products e.g. 'S2MSI1C', 'S2MSI2A'
Product_Type = 'S2MSI2A'
# Set a limit to the cloud cover percentage (%)
Cloud_Cover = (0,1)
# Search for all suitable products
products = api.query(area=AOI, date=(START, END), producttype=Product_Type, cloudcoverpercentage=Cloud_Cover)

# Output all results
for i in products:
    product = products[i]
    filename = product['filename']
    print(filename)

# Download all results from the search
# Note: up to two products can be downloaded at the same time
downloadfiles = api.download_all(products)