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
from numpy import vectorize
from geopy import distance

# Load in the data
school_df = pd.read_csv('data/qld-school-listings.csv')
# Get rid of all NaN values
school_df = school_df.fillna('')

# Constrain the plotted points to a radial distance around the centre of the map
map_centre_lat = -27.466219
map_centre_long = 153.026354
critical_dist = 10 # kilometers of circle around map centre to select schools
map_centre = (map_centre_lat, map_centre_long)

def pt_in_radius(lat, long):
    dist = distance.distance(map_centre, (lat, long)).km
    if dist < critical_dist:
        return True
    else:
        return False

school_df['in_radius'] = vectorize(pt_in_radius)(school_df['Latitude'], school_df['Longitude'])

# Eliminate all points outside the radius
school_df = school_df[school_df['in_radius']==True]

# Define the base map
m = folium.Map(location=[map_centre_lat, map_centre_long], zoom_start=14) # Centre brisbane CBD


# Combine the address into a cohesive string
def address_helper(number, street, suburb):
    if number=='' and street=='':
        return suburb
    elif number=='':
        return street + ', ' + suburb
    else:
        return number + ' ' + street + ', ' + suburb


school_df['address'] = vectorize(address_helper)(school_df['Actual Street Number'], school_df['Actual Street Name'], school_df['Actual Suburb/Town'])

# Add the Schools as points
fg = folium.FeatureGroup(name="School Locations")

loop_obj = zip(school_df['Latitude'], school_df['Longitude'], school_df['School Name'], school_df['address'], school_df['Phone Number'], school_df['Internet Site'])

# Linkify lambda function. New Tab with clickable link
linkify = lambda x: '<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"http://{0}\">{0}</a>'.format(x) if x!='' else ''

for lat, long, name, addr, phone, web in loop_obj:
    # TODO Separate markers based on the school category on the map
    table_df = pd.DataFrame(data=[[name], [addr], [phone], [web]],
                            index=['Name', 'Address', 'Phone', 'Website'])
    table_html = table_df.to_html(classes='table table-striped table-hover table-condensed table-responsive',
                                  header=False)

    # Ghetto way to add the link embedded link into the html and lowercase the link
    table_html = table_html.replace(web, linkify(web.lower()))
    popup = folium.Popup(html=table_html)
    fg.add_child(folium.Marker(location=[lat, long], popup=table_html, tooltip=name))

m.add_child(fg)

# Add in a red circle for the radius of the schools
folium.Circle([map_centre_lat, map_centre_long], critical_dist*1000, color='#FF0000').add_to(m)

# Add in the Layer Control so that we can trigger on and off layers
folium.LayerControl(collapsed=False).add_to(m)

m.save(os.path.join('map_results', 'map.html'))

