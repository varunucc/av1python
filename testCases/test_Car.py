from unittest import TestCase
from avSystem.Car import CarStatusEnums
from testFunctions.CarTestVarun import *


class TestCar(TestCase):

    def test_action_according_to_traffic_signal_colour_and_distance(self):
        # self.assertEqual(actionAccordingToTrafficSignalColourAndDistance(0, 80, "Red"), CarStatusEnums.within80ButSpeedLessThan30)
        self.assertEqual(actionAccordingToTrafficSignalColourAndDistance(70, 1, "Red"), CarStatusEnums.stopping)
