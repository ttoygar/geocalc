import csv
import datetime
import json
from math import radians, cos, sin, asin, sqrt
from typing import Tuple

import geopy
from flask import Blueprint, render_template, request
from shapely.geometry import Point, shape, Polygon
from shapely.ops import nearest_points

geocalc = Blueprint("geocalc", __name__, static_folder='static', template_folder='templates')


@geocalc.route("/")
def calc() -> str:
    addr: str = request.args.get('address')
    if addr is None: addr = "А107, Moskovskaya oblast', Rusya, 142410"

    distance: float
    lat1: float
    lon1: float
    lat2: float
    lon2: float

    distance, lat1, lon1, lat2, lon2 = distance_calc(addr, mkad_coords)

    if distance == 0: return "<h1>Selected address is inside MKAD </h1>"

    write_files(addr, lat1, lon1, lat2, lon2, distance)
    return render_template("index.html", distance=distance)


# addr = "А107, Moskovskaya oblast', Rusya, 142410"
# addr : str = ""
# point = Point(38.42442512512207, 55.82491258016849)

mkad_coords = "mkad.geojson"
locator = geopy.ArcGIS()  # type: geocoders


def mkad_poly_calc(mkad_crds: str = mkad_coords) -> Polygon:
    with open(mkad_crds) as f:
        #   features = json.load(f)["features"]
        js = json.load(f)

    for feature in js['features']:
        mkad_poly = shape(feature['geometry'])
    return mkad_poly


def point_calc(address: str, locator=geopy.ArcGIS()) -> Point:
    location = locator.geocode(address)
    point = Point(location.longitude, location.latitude)
    return point


def haversine(lati1: float, long1: float, lati2: float, long2: float) -> float:
    R: float = 6372.8  # 3959.87433  this is in miles.  For Earth radius in kilometers use 6372.8 km

    d_lat: float = radians(lati2 - lati1)
    d_lon: float = radians(long2 - long1)
    lati1: float = radians(lati1)
    lati2: float = radians(lati2)

    a: float = sin(d_lat / 2) ** 2 + cos(lati1) * cos(lati2) * sin(d_lon / 2) ** 2
    c: float = 2 * asin(sqrt(a))

    return R * c


# Usage
# lon1 = 37.84326553344727
# lat1 = 55.77149195159078
# lon2 = 38.42442512512207
# lat2 = 55.82491258016849

def distance_calc(addr: str, mkad_coords: str = mkad_coords) -> Tuple[float, float, float, float, float]:
    poly: Polygon = mkad_poly_calc(mkad_coords)
    point: Point = point_calc(addr, locator=geopy.ArcGIS())

    if poly.contains(point): return 0, 0, 0, 0, 0

    p1: Point
    p2: Point
    p1, p2 = nearest_points(poly, point)

    lon1: float = p1.x
    lat1: float = p1.y
    lon2: float = p2.x
    lat2: float = p2.y

    distance: float = haversine(lat1, lon1, lat2, lon2)
    return distance, lat1, lon1, lat2, lon2


# distance, lat1, lon1, lat2, lon2 = distance_calc(addr, mkad_coords)


def write_files(addr:str, lat1:float, lon1:float, lat2:float, lon2:float, distance:float) -> None:
    # Writing to files
    fields:list = [datetime.datetime.utcnow(), addr, lat1, lon1, lat2, lon2, distance]

    with open(r'geoc.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(fields)

    with open(r'geoc.log', 'a', encoding='utf-8') as file:
        file.write(str(distance) + "\n")
