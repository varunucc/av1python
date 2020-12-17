from unittest import TestCase
from testFunctions.TrafficSignalTestVarun import *
from avSystem.Main import TrafficSignalEnum


class TestTrafficSignal(TestCase):

    def test_rotate_signals_1(self):
        trafficSignalList = [TrafficSignalEnum, TrafficSignalEnum]
        self.assertIsInstance(rotateSignals(0, trafficSignalList), TrafficSignalEnum)

    def test_next_signal(self):
        trafficSignalList = [TrafficSignalEnum]
        self.assertEqual(goToNextSignalAndSetLocation(1, trafficSignalList), -1)
