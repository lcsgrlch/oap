"""
Testing all methods from oap.utils.sizing
"""

import unittest
import oap

from tests.data import array01_original as array


class TestUtilsSizing(unittest.TestCase):

    def test_xy_diameter(self):
        x, y = oap.xy_diameter(array)
        self.assertEqual(x, 43)
        self.assertEqual(y, 45)

    def test_x_diameter(self):
        self.assertEqual(oap.x_diameter(array), 43)

    def test_y_diameter(self):
        self.assertEqual(oap.y_diameter(array), 45)

    def test_min_diameter(self):
        self.assertEqual(round(oap.min_diameter(array), 10), 49.6358592054)

    def test_max_diameter(self):
        self.assertEqual(round(oap.max_diameter(array), 10), 62.2414652784)

    def test_area_ratio(self):
        pass

    def test_sphere_volume(self):
        self.assertEqual(round(oap.sphere_volume(diameter=9.2), 6), 407.720083)
        self.assertEqual(round(oap.sphere_volume(diameter=15.3), 5), 1875.30933)
        self.assertEqual(round(oap.sphere_volume(diameter=42.0), 4), 38792.3861)

    def test_sphere_surface(self):
        self.assertEqual(round(oap.sphere_surface(diameter=9.2), 6), 265.904402)
        self.assertEqual(round(oap.sphere_surface(diameter=15.3), 6), 735.415424)
        self.assertEqual(round(oap.sphere_surface(diameter=42.0), 5), 5541.76944)

    def test_hexprism_volume(self):
        self.assertEqual(round(oap.hexprism_volume(height=3.5, diameter=2.4), 12), 13.094304105221)
        self.assertEqual(round(oap.hexprism_volume(height=9.8, diameter=8.2), 11), 428.00187890592)
        self.assertEqual(round(oap.hexprism_volume(height=16.7, diameter=14.6), 10), 2312.1397377604)

    def test_hexprism_surface(self):
        self.assertEqual(round(oap.hexprism_surface(height=3.5, diameter=2.4), 12), 32.682459488698)
        self.assertEqual(round(oap.hexprism_surface(height=9.8, diameter=8.2), 11), 328.4273222257)
        self.assertEqual(round(oap.hexprism_surface(height=16.7, diameter=14.6), 9), 1008.362962606)
