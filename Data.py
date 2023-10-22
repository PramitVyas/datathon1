import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import geopandas as gpd
import random


df = pd.read_csv('roger.csv')

columns_to_drop = ['network.id', 'date']
df.drop(columns_to_drop, axis=1, inplace=True)

df

df['Infolink.Direction'] = df['Infolink.Direction'].str.upper()

def check_location(row):
    if row['Infolink.Direction'] == 'N' and row['Latitude'] > 41.5868:
        return 'Leaving'
    elif row['Infolink.Direction'] == 'S' and row['Latitude'] < 41.5868:
        return 'Leaving'
    elif row['Infolink.Direction'] == 'W' and row['Longitude'] < -93.6250:
        return 'Leaving'
    elif row['Infolink.Direction'] == 'E' and row['Longitude'] > -93.650:
        return 'Leaving'
    else:
        return 'Coming'

# Apply the function to each row and create a new column 'location'
df['location'] = df.apply(check_location, axis=1)

# Convert the 'date' column to datetime format
df['cdate'] = pd.to_datetime(df['cdate'])


start_date = '2022-11-23'
end_date = '2022-11-24'

# Subset the data based on date range
subset_df_before = df[(df['cdate'] >= start_date) & (df['cdate'] < end_date)]


# Define the coordinates of Des Moines
des_moines_coords = [41.5868, -93.6250]

iowa_boundary_geojson = 'County_boundary_GeoJSON.geojson' 

# Create a map centered on Des Moines
des_moines_map = folium.Map(location=des_moines_coords, zoom_start=13)

# Add a marker for Des Moines
folium.Marker(des_moines_coords, popup='Des Moines').add_to(des_moines_map)

# Load the GeoJSON file for boundaries (replace with your file path)
geojson_file = 'County_boundary_GeoJSON.geojson'

# Add the GeoJSON layer to the map
folium.GeoJson(geojson_file, name='Iowa Boundary').add_to(des_moines_map)

# Create a heatmap for each category
categories = subset_df_before['location'].unique()
for category in categories:
    category_data = subset_df_before[subset_df_before['location'] == category]

     # Create a HeatMap with folium.plugins
    heat_data = [[row['Latitude'], row['Longitude']] for index, row in category_data.iterrows()]
    folium.plugins.HeatMap(heat_data).add_to(des_moines_map)

    # Save the map with the heatmap, marker, and GeoJSON as an HTML file
    des_moines_map.save(f'des_moines_heatmap_{category}_before.html')


#### After thanksgiving 
start_date = '2022-11-24'
end_date = '2022-11-25'
subset_df_after = df[(df['cdate'] > start_date) & (df['cdate'] <= end_date)]


categories = subset_df_after['location'].unique()
for category in categories:
    category_data = subset_df_after[subset_df_after['location'] == category]

     # Create a HeatMap with folium.plugins
    heat_data = [[row['Latitude'], row['Longitude']] for index, row in category_data.iterrows()]
    folium.plugins.HeatMap(heat_data).add_to(des_moines_map)

    # Save the map with the heatmap, marker, and GeoJSON as an HTML file
    des_moines_map.save(f'des_moines_heatmap_{category}_after.html')




