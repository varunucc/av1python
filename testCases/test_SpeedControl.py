from unittest import TestCase
from testFunctions.SpeedControlTestVarun import *


class TestSpeedControl(TestCase):

    def test_calculate_deceleration_rate_within_distance_1(self):
        self.assertEqual(calculateDecelerationRateWithinDistanceForTesting(60, 30, 60), -1.7361111111111114)

    def test_calculate_deceleration_rate_within_distance_2(self):
        self.assertRaises(Exception, calculateDecelerationRateWithinDistanceForTesting(0, 0, 0))

    def test_accelerate_1(self):
        self.assertEqual(accelerate(1, 60, 50), 53.6)

    def test_accelerate_2(self):
        with self.assertRaises(ValueError):
            self.assertRaises(ValueError, accelerate(0, 60, 50))

    def test_decelerate_1(self):
        self.assertEqual(decelerate(-1, 30, 50), 46.4)

    def test_decelerate_2(self):
        with self.assertRaises(ValueError):
            self.assertRaises(ValueError, decelerate(0, 0, 30))
