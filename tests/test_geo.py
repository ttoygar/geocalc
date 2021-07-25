import os, sys
import tempfile

import pytest
import unittest
from flask import Flask

root = os.path.dirname(os.getcwd())
sys.path.append(root)

from fgeocoder import create_app
# from fgeocoder.geocalc import geocalc
# from fgeocoder import geocalc as geo
# from fgeocoder.geocalc.geocalc import geocalc
from fgeocoder.geocalc import geocalc as geo

# print(os.path.isfile(os.path.join(os.getcwd(),"fgeocoder", "geocalc","mkad.geojson")))
# print(os.path.abspath("../fgeocoder/mkad.geojson"))

# @pytest.fixture
# def client():
#     client = geocalc.
#     yield client


class GeocoderTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # pass
        # app.app.testing = True
        # self.app = app.app.test_client()
        # self.app = Flask(__name__)

    def tearDown(self) -> None:
        pass

    def test_response(self):
        # app = Flask(__name__)
        # app.register_blueprint(geocalc, url_prefix='/')
        # web = app.test_client()
        response = self.client.get('/')
        assert response.status_code, 200
        assert 'HTML' in response.data.decode('utf-8')
        # self.assertEqual(response.headers['content-type'], "text/html; charset=utf-8")

    def test_mkad_file(self):
        m_file = os.path.join(os.path.dirname(os.getcwd()), "fgeocoder",
                              "geocalc", "mkad.geojson")
        print(os.path.isfile(m_file))
        print(m_file)
        self.assertTrue(
            os.path.isfile(m_file))
        with open(m_file, "r") as file:
            self.assertEqual(file.read(50),
                             '{"type":"FeatureCollection","features":[{'
                             '"type":"F')

    def test_poly(self):
        poly_test = geo.mkad_poly_calc()
        self.assertEqual(poly_test.geom_type, 'Polygon')
        self.assertEqual(str(geo.mkad_poly_calc())[:50],
                         "POLYGON ((37.84026145935059 55.79831394954606, 37.")

    def test_points(self):
        location = geo.LOCATOR.geocode("Ankara")
        self.assertAlmostEqual(location.latitude, 39.9211, places=3)
        self.assertAlmostEqual(location.longitude, 32.8539, places=3)

    def test_haversine(self):
        self.assertAlmostEqual(geo.haversine(1, 2, 3, 4), 314.4918, places=3)

    def test_distances_app(self):
        addresses = ["А107, Moskovskaya oblast', Rusya, 142410",
                     "Pushkinsky District, Moskova Oblastı, Rusya, 141273",
                     "Ярославское ш., 47 км, Московская обл., 141273"]
        confirms = [36.775, 33.981, 32.043]
        results = [geo.distance_calc(address)[0] for address in addresses]
        for i in range(len(confirms)):
            self.assertAlmostEqual(confirms[i], results[i], places=3)

    def test_distances_browser(self):
        addresses = ["Ankara",
                     "А107, Moskovskaya oblast', Rusya, 142410",
                     "Pushkinsky District, Moskova Oblastı, Rusya, 141273",
                     "Ярославское ш., 47 км, Московская обл., 141273"]
        confirms = ["<h1>1776.","<h1>36.7", "<h1>33.9", "<h1>32.0"]
        for i in range(len(addresses)):
            response = self.client.get(f"/?address={addresses[i]}")
            self.assertIn(confirms[i], response.data.decode('utf-8'), msg=f"address: {addresses[i]}")

    def test_corner_cases(self):
        # empty query
        for mark in "+.,-/_-|":
            query = f"/?address={mark}"
            response = self.client.get(query)
            self.assertEqual(response.status, "200 OK", msg=f"Problematic query found: {mark}")