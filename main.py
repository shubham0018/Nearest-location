"""
Created on Fri Nov  6 13:04:22 2020

@author: shubham
"""
# Need to install 3 packages -
# 1. 'GoogleMaps' - for using requests
# 2. 'geopy' - used for calculating distance b/w 2 locations
# 3. 'gmplot' - for plotting locations in GoogleMap and saving as map.html
import requests
import urllib.parse
from geopy.distance import geodesic
import sys
import gmplot

# Given places
attractions_lats, attractions_lngs = zip(*[
    (12.8996676, 77.4826837),
    (12.9044382, 77.5649278),
    (12.9981732, 77.5530446),
    (13.0323448, 77.5697877),
    (12.9165757, 77.6101163),
    (12.8452145, 77.6601695),
    (12.9304278, 77.678404),
    (12.9689968, 77.7208853)
])
print("Enter the location")
address = str(input())
# "Jss academy of technical education, Bengaluru"

# Getting latitude and longitude of given location
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
response = requests.get(url).json()
loc2 = (float(response[0]["lat"]), float(response[0]["lon"]))

minimum = sys.float_info.max
k = 0
for (i, j)in zip(attractions_lats, attractions_lngs):
    if((geodesic((i, j), loc2).meters) < minimum):
        minimum = geodesic((i, j), loc2).meters
        lat, lng = i, j
closest_loc = str(lat)+","+str(lng)

# Getting name of closest location
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(closest_loc) +'?format=json'
response = requests.get(url).json()
closest = response[0]['display_name']

# Printing the output
print(f'The closest location from "{address}" is "{closest}" and distance is {round(minimum, 2)} meters')
print("You can view the generated map.html file for more details...")

# Plotting the points in map with shortest distant location from given location
# Create the map plotter:
apikey = 'AIzaSyDeRNMnZ__VnQDiATiuz4kPjF_c9r1kWe8' # (your API key here)
gmap = gmplot.GoogleMapPlotter(12.95396, 77.4908527, 14, apikey=apikey)

# Mark a hidden gem:
gmap.marker(loc2[0], loc2[1], color='blue')

#Marking all given locations
gmap.scatter(attractions_lats, attractions_lngs, color='red', size=400, marker=True)

# Creating a line between nearest point:
line = zip(*[
    loc2,
    (lat, lng)
])

gmap.polygon(*line, color='cyan', edge_width=5)

# Draw the map to an HTML file (will be saved in same directory as the main file)
# Can be used to view all the locations and shortest distance found above
gmap.draw('map.html')
