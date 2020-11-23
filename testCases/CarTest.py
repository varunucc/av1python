import unittest
from Models.Car import Car
from Models.TrafficSignal import currentSignal
from Models.TrafficSignal import TrafficSignalEnum


class CarTest(unittest.TestCase):

    def signalTypeTest(self):
        car = Car()
        car.main()
        try:
            self.assertIsInstance(currentSignal, TrafficSignalEnum)
            print("Passed")
        except:
            print("Error")





test = CarTest()
test.signalTypeTest()

