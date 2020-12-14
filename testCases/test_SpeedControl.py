from unittest import TestCase
from avSystem.SpeedControl import SpeedControl
from example_code import mul

class TestSpeedControl(TestCase):

    def test_slow_down_vehicle_speed(self):
        self.assertEqual(0, 0)

    def test_bring_vehicle_to_halt(self):
        self.assertEqual(0, 0)

    def test_calculate_acceleration_rate_to_limited_speed(self):
        self.assertEqual(0, 0)

    def test_calculate_deceleration_rate_within_distance(self):
        self.assertGreater(1, 0)

    def test_accelerate(self):
        sc = SpeedControl()
        self.assertEqual(sc.accelerate(1, 60, 50), 54)

    def multiple(self):
        self.assertEqual(mul(2, 3), 6)

    def test_decelerate(self):
        self.assertEqual(0, 0)

    def test_changed_vehicle_speed(self):
        self.assertEqual(0, 0)

    def test_changed_vehicle_speed(self):
        self.assertEqual(0, 0)

    def test_notify_speed_change(self):
        self.assertEqual(0, 0)
