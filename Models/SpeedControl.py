import threading
import time

changedVehicleSpeed = 0


class SpeedControl:
    def __init__(self):
        print("SpeedControl")
        self._observers = []
        self._changedVehicleSpeed = 0

    def slowDownVehicleSpeed(self, vehicleSpeed, speedLimitedTo):
        self.calculateDecelerationRateToLimitedSpeed(vehicleSpeed, speedLimitedTo)

    def bringVehicleToHalt(self, vehicleSpeed, speedLimitedTo):
        print("BringVehicleToHalt")

    def calculateAccelerationRateToLimitedSpeed(self, vehicleSpeed, speedLimitedTo):
        self.accelerate(1, speedLimitedTo, vehicleSpeed)

    def calculateDecelerationRateToLimitedSpeed(self, vehicleSpeed, speedLimitedTo):
        # TODO calculate deceleration rate
        decelerationRate = 0.5
        self.decelerate(decelerationRate, vehicleSpeed, speedLimitedTo)

    def accelerate(self, accelerateRate, speedLimitedTo, vehicleSpeed):
        print("Accelerating..")
        while vehicleSpeed <= speedLimitedTo:
            time.sleep(accelerateRate)
            vehicleSpeed += 1
            global changedVehicleSpeed
            self.changedVehicleSpeed = vehicleSpeed
            print("Speed: ", self.changedVehicleSpeed)

    def decelerate(self, decelerateRate, speedLimitedTo, vehicleSpeed):
        print("Decelerating..")
        while vehicleSpeed >= speedLimitedTo:
            time.sleep(decelerateRate)
            vehicleSpeed -= 1
            global changedVehicleSpeed
            self.changedVehicleSpeed = vehicleSpeed
            print("Speed: ", self.changedVehicleSpeed)

    @property
    def changedVehicleSpeed(self):
        print("got speed changed")
        return self._changedVehicleSpeed

    @changedVehicleSpeed.setter
    def changedVehicleSpeed(self, new_value):
        print("set changed speed")
        self._changedVehicleSpeed = new_value
        for callback in self._observers:
            callback(self._changedVehicleSpeed)

    def notifySpeedChange(self, callback):
        self._observers.append(callback)