"""
Testing all methods from oap.utils
"""

import unittest
import oap

from tests.data import (
    array01_barycenter_coordinates,
    array01_original,
    array01_adjust01,
    array01_adjust02,
    array01_toclip01,
    array01_move_x01,
    array01_move_x02,
    array01_move_y01,
    array01_move_y02
)


class TestUtils(unittest.TestCase):

    def test_barycenter(self):
        self.assertEqual(oap.barycenter(array01_original), array01_barycenter_coordinates)

    def test_adjust_y(self):
        self.assertEqual(oap.adjust_y(array01_original, new_y=49), array01_adjust01)
        self.assertEqual(oap.adjust_y(array01_original, new_y=14), array01_adjust02)

    def test_clip_y(self):
        # self.assertEqual(oap.clip_y(array01_toclip01), array01_original)
        pass

    def test_flip_x(self):
        pass

    def test_flip_y(self):
        pass

    def test_monochromatic(self):
        pass

    def test_monoscale(self):
        pass

    def test_move_to_x(self):
        self.assertEqual(oap.move_to_x(array01_original, new_x=12), array01_move_x01)
        self.assertEqual(oap.move_to_x(array01_original, new_x=56), array01_move_x02)

    def test_move_to_y(self):
        self.assertEqual(oap.move_to_y(array01_original, new_y=4), array01_move_y01)
        self.assertEqual(oap.move_to_y(array01_original, new_y=43), array01_move_y02)
