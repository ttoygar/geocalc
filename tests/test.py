import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)
print(root)

from flask import Flask
import unittest
from fgeocoder.geocalc import geocalc
from fgeocoder import geocalc as geo


class GeocoderTestCase(unittest.TestCase):

    def setUp(self):
        pass
        # app.app.testing = True
        # self.app = app.app.test_client()
        # self.app = Flask(__name__)

    def tearDown(self) -> None:
        pass

    def test_response(self):
        app = Flask(__name__)
        app.register_blueprint(geocalc, url_prefix='/')
        web = app.test_client()
        response = web.get('/')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.headers['content-type'], "text/html; charset=utf-8")

    def test_mkad_file(self):
        self.assertTrue(os.path.isfile(os.path.abspath("../fgeocoder/mkad.geojson")))
        with open("mkad.geojson", "r") as file:
            self.assertEqual(file.read(50), '{"type":"FeatureCollection","features":[{"type":"F')

    def test_poly(self):
        poly_test = geo.mkad_poly_calc()
        self.assertEqual(poly_test.geom_type, 'Polygon')
        self.assertEqual(str(geo.mkad_poly_calc())[:50], "POLYGON ((37.84026145935059 55.79831394954606, 37.")

    def test_points(self):
        self.assertIn("geopy.geocoders.arcgis.ArcGIS", str(geo.locator))
        location = geo.locator.geocode("Ankara")
        self.assertAlmostEqual(location.latitude, 39.9211, places=3)
        self.assertAlmostEqual(location.longitude, 32.8539, places=3)

    def test_haversine(self):
        self.assertAlmostEqual(geo.haversine(1, 2, 3, 4), 314.4918, places=3)

    def test_distances(self):
        addresses = ["А107, Moskovskaya oblast', Rusya, 142410",
                     "Pushkinsky District, Moskova Oblastı, Rusya, 141273",
                     "Ярославское ш., 47 км, Московская обл., 141273"]
        confirms = [36.775, 33.981, 32.043]
        results = [geo.distance_calc(address)[0] for address in addresses]
        for i in range(len(confirms)):
            self.assertAlmostEqual(confirms[i], results[i], places=3)
