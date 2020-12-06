import unittest
from avSystem.Car import Car
from avSystem.TrafficSignal import currentSignal
from avSystem.Main import TrafficSignalEnum1


class CarTest(unittest.TestCase):

    def signalTypeTest(self):
        car = Car()
        car.main()
        try:
            self.assertIsInstance(currentSignal, TrafficSignalEnum1)
            print("\nPassed")
        except:
            print("\nError")





test = CarTest()
test.signalTypeTest()

