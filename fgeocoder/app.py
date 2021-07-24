from flask import Flask, render_template, request
from geocalc import geocalc
import json
from shapely.geometry import Point, shape
from shapely.ops import nearest_points
from math import radians, cos, sin, asin, sqrt
import geopy
import csv, datetime


# # addr = "А107, Moskovskaya oblast', Rusya, 142410"
# # addr : str = ""
# # point = Point(38.42442512512207, 55.82491258016849)
#
# mkad_coords = "mkad.geojson"
# locator=geopy.ArcGIS()
#
#
# def mkad_poly_calc(mkad_crds=mkad_coords):
#     with open(mkad_crds) as f:
#         #   features = json.load(f)["features"]
#         js = json.load(f)
#
#     for feature in js['features']:
#         mkad_poly = shape(feature['geometry'])
#     return mkad_poly
#
#
# def point_calc(address, locator=geopy.ArcGIS()):
#     location = locator.geocode(address)
#     point = Point(location.longitude, location.latitude)
#     return point
#
#
# def haversine(lati1, long1, lati2, long2):
#     R = 6372.8  # 3959.87433  this is in miles.  For Earth radius in kilometers use 6372.8 km
#
#     d_lat = radians(lati2 - lati1)
#     d_lon = radians(long2 - long1)
#     lati1 = radians(lati1)
#     lati2 = radians(lati2)
#
#     a = sin(d_lat / 2) ** 2 + cos(lati1) * cos(lati2) * sin(d_lon / 2) ** 2
#     c = 2 * asin(sqrt(a))
#
#     return R * c
#
#
# # Usage
# # lon1 = 37.84326553344727
# # lat1 = 55.77149195159078
# # lon2 = 38.42442512512207
# # lat2 = 55.82491258016849
#
# def distance_calc(addr, mkad_coords=mkad_coords):
#     poly = mkad_poly_calc(mkad_coords)
#     point = point_calc(addr, locator=geopy.ArcGIS())
#
#     if poly.contains(point):
#         return None
#
#     p1, p2 = nearest_points(poly, point)
#
#     lon1 = p1.x
#     lat1 = p1.y
#     lon2 = p2.x
#     lat2 = p2.y
#
#     distance = haversine(lat1, lon1, lat2, lon2)
#     return distance, lat1, lon1, lat2, lon2
#
#
# # distance, lat1, lon1, lat2, lon2 = distance_calc(addr, mkad_coords)
# def write_files(addr, lat1, lon1, lat2, lon2, distance):
#     # Writing to files
#     fields = [datetime.datetime.utcnow(), addr, lat1, lon1, lat2, lon2, distance]
#
#     with open(r'geoc.csv', 'a', encoding='utf-8') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow(fields)
#
#     with open(r'geoc.log', 'a', encoding='utf-8') as file:
#         file.write(str(distance) + "\n")

app = Flask(__name__)
app.register_blueprint(geocalc, url_prefix='')

@app.route("/")
def index():
    # addr = request.args.get('address')
    # distance, lat1, lon1, lat2, lon2 = distance_calc(addr, mkad_coords)
    # write_files(addr, lat1, lon1, lat2, lon2, distance)
    # return render_template("index.html", distance=distance)
    return "Original page"
