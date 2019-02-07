# Tutorial guidance inspired heavily by https://pythonhow.com/web-mapping-with-python-and-folium/
# Using data from the QLD open data portal https://data.qld.gov.au/

#TODO feature idea. search bar on school name to activate tooltip
#TODO feature idea choropleth map, with changes in time for attendance rates
# https://data.qld.gov.au/dataset/state-school-attendance-rate/resource/f8ceabd3-d61c-4714-87de-0bc9254e7c08
# https://www.kaggle.com/daveianhickey/how-to-folium-for-maps-heatmaps-time-analysis
# https://blog.dominodatalab.com/creating-interactive-crime-maps-with-folium/


import folium
import pandas as pd
import os

# Load in the data
school_df = pd.read_csv('data/qld-school-listings.csv')

#TODO constrain schools to within a radius around a central point
# geopy distance module  geopy.distance.distance()

map_centre_lat = -27.466219
map_centre_long = 153.026354
m = folium.Map(location=[map_centre_lat, map_centre_long], zoom_start=12) # Centre brisbane CBD

#TODO Make a html table add to each school with Name, Address, Phone, Website
# https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/Popups.ipynb

# Add the Schools as points
fg = folium.FeatureGroup(name="School Locations")

for lat, long, name in zip(school_df['Latitude'], school_df['Longitude'], school_df['School Name']):
    # TODO Seperate markers based on the school category on the map
    fg.add_child(folium.Marker(location=[lat, long], popup=folium.Popup(name), tooltip=name))

m.add_child(fg)
m.save(os.path.join('map_results', 'map.html'))

