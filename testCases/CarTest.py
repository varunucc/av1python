import unittest
from Models.Car import Car
from Models.TrafficSignal import currentSignal
from Models.Main import TrafficSignalEnum1


class CarTest(unittest.TestCase):

    def signalTypeTest(self):
        car = Car()
        car.main()
        try:
            self.assertIsInstance(currentSignal, TrafficSignalEnum1)
            print("Passed")
        except:
            print("Error")





test = CarTest()
test.signalTypeTest()

