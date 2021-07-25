import csv
import datetime
import json
import os
from math import radians, cos, sin, asin, sqrt
from typing import Tuple

import geopy
from geopy import geocoders
from flask import Blueprint, render_template, request
from shapely.geometry import Point, shape, Polygon
from shapely.ops import nearest_points

geocalc = Blueprint("geocalc", __name__, static_folder='static',
                    template_folder='templates')

MKAD_COORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mkad.geojson")  # MKAD coordinates geojson file.
LOCATOR: geocoders = geopy.ArcGIS()  # Geocoder to use.
R: float = 6372.8  # Radius of Earth. 3959.87433 miles or 6372.8 km


@geocalc.route("/")
def calc() -> str:
    """Returns the HTML code to be displayed and provides the address
    information from HTTP request to other functions.

            Returns: HTML code to display
    """
    addr: str = request.args.get('address')
    if addr is None: addr = "А107, Moskovskaya oblast', Rusya, 142410"

    distance: float
    lat1: float
    lon1: float
    lat2: float
    lon2: float

    distance, lat1, lon1, lat2, lon2 = distance_calc(addr, MKAD_COORDS_FILE)

    if distance == 0:
        return "<h1>Selected address is inside MKAD </h1>"

    write_files(addr, lat1, lon1, lat2, lon2, distance)
    return render_template("index.html", distance=distance)


def mkad_poly_calc(mkad_crds: str = MKAD_COORDS_FILE) -> Polygon:
    """Creates a polygon from a .geojson file."""
    with open(mkad_crds) as f:
        #   features = json.load(f)["features"]
        js = json.load(f)

    for feature in js['features']:
        mkad_poly = shape(feature['geometry'])
    return mkad_poly


def point_calc(address: str, locator=LOCATOR) -> Point:
    """Calculates coordinates from an address using a geocoder."""
    location = locator.geocode(address)
    point = Point(location.longitude, location.latitude)
    return point


def haversine(lati1: float, long1: float, lati2: float, long2: float,
              r: float = R) -> float:
    """Calculates the haversine distance using two points' latitude
    and longitude coordinates and Earth's radius.

            Parameters:
                lati1 (float): latitude of first point
                long1 (float): longitude of first point
                lati2 (float): latitude of second point
                long2 (float): longitude of second point
                r (float): Earth's radius. Default R=6372.8 km

            Returns:
                haversine_distance (float): Calculated haversine distance
    """
    d_lat: float = radians(lati2 - lati1)
    d_lon: float = radians(long2 - long1)
    lati1: float = radians(lati1)
    lati2: float = radians(lati2)

    a: float = sin(d_lat / 2) ** 2 + cos(lati1) * \
               cos(lati2) * sin(d_lon / 2) ** 2
    c: float = 2 * asin(sqrt(a))
    haversine_distance: float = r * c

    return haversine_distance


def distance_calc(addr: str,
                  mkad_coords: str = MKAD_COORDS_FILE,
                  locator: geocoders = LOCATOR) \
        -> Tuple[float, float, float, float, float]:
    """
    Calculates nearest haversine distance and nearest
    point coordinates using address and polygon coordinates.

            Parameters:
                addr (int): Given address
                mkad_coords (str): Name of the .geojson file
                locator (str): Geocoder to be used. Default ArcGIS

            Returns:
                distance (float): Haversine distance between address
                    and the nearest point of given polygon coordinates.
                lat1 (float): latitude of nearest polygon point
                lon1 (float): longitude of nearest polygon point
                lat2 (float): latitude of address
                lon2 (float): longitude of address

     """
    poly: Polygon = mkad_poly_calc(mkad_coords)
    point: Point = point_calc(addr, locator)

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


def write_files(addr: str, lat1: float, lon1: float, lat2: float,
                lon2: float, distance: float) -> None:
    """Writes related information to geoc.csv and geoc.log files."""
    fields: list = [datetime.datetime.utcnow(), addr, lat1, lon1,
                    lat2, lon2, distance]

    with open(r'geoc.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(fields)

    with open(r'geoc.log', 'a', encoding='utf-8') as file:
        file.write(str(distance) + "\n")
