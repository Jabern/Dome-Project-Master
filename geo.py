import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from io import StringIO

# Example textual representation of fictional country boundaries
text_representation = '''
Country Name,Geometry
Country A,"POLYGON ((0 0, 0 5, 3 3, 5 5, 5 0, 0 0))"
Country B,"POLYGON ((3 3, 3 8, 6 6, 8 8, 8 3, 3 3))"
Country C,"POLYGON ((7 7, 7 10, 10 10, 10 7, 7 7))"
'''

# Read the textual representation into a pandas DataFrame
df = pd.read_csv(StringIO(text_representation))

# Convert the string geometries to Shapely Polygon objects
df['Geometry'] = df['Geometry'].apply(lambda geom: Polygon([tuple(map(float, coord.split())) for coord in geom[10:-2].split(',')]))

# Create a GeoDataFrame with the geometry column
gdf = gpd.GeoDataFrame(df, geometry='Geometry')

# Save the GeoDataFrame as a GeoJSON file
gdf.to_file('fictional_countries.geojson', driver='GeoJSON')
