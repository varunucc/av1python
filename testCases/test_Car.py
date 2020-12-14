from unittest import TestCase
from avSystem.Main import TrafficSignalEnum1


class TestCar(TestCase):

    def test_check_traffic_light_colour(self, signalColour):
        self.assertIsInstance(signalColour, TrafficSignalEnum1)

    def test_set_road_length_covered(self):
        self.fail()

    def test_set_traffic_signal_location(self):
        self.fail()

    def test_check_distance_to_traffic_signal(self):
        self.fail()

    def test_set_speed_limited_to(self):
        self.fail()

    def test_action_according_to_traffic_signal_colour_and_distance(self):
        self.fail()

    def test_failure_to_reduce_speed_before20mts_check(self):
        self.fail()

    def test_set_vehicle_speed(self):
        self.fail()
