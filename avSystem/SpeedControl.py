import threading
import time

changedVehicleSpeed = 0


class SpeedControl:
    def __init__(self):
        # print("SpeedControl")
        self._observers = []
        self._changedVehicleSpeed = 0
        self.accelerating = False
        self.slowDown = False
        self.stop = False
        self.accelerationRate = 1
        self.decelerationRate = 0.5

    def slowDownVehicleSpeed(self, vehicleSpeed, speedLimitedTo, distanceToSlowDownWithin):
        self.calculateDecelerationRateWithinDistance(vehicleSpeed, speedLimitedTo, distanceToSlowDownWithin)

    def bringVehicleToHalt(self, vehicleSpeed, speedLimitedTo, distanceToHaltWithin):
        self.calculateDecelerationRateWithinDistance(vehicleSpeed, speedLimitedTo, distanceToHaltWithin)

    def calculateAccelerationRateToLimitedSpeed(self, vehicleSpeed, speedLimitedTo):
        self.accelerate(self.accelerationRate, speedLimitedTo, vehicleSpeed)

    def calculateDecelerationRateWithinDistance(self, vehicleSpeed, speedLimitedTo, distanceWithin):
        # TODO calculate deceleration rate
        decelerationRate = 0.5
        self.decelerate(decelerationRate, speedLimitedTo, vehicleSpeed)

    def accelerate(self, accelerateRate, speedLimitedTo, vehicleSpeed):
        # print("Accelerating..")
        # print("Accelerating value: ", self.accelerating)
        while self.accelerating:
            time.sleep(accelerateRate)
            # convert to km/hr
            if vehicleSpeed < speedLimitedTo:
                vehicleSpeed += 1 * 3.6
            global changedVehicleSpeed
            self.changedVehicleSpeed = vehicleSpeed
            # print("Speed: ", self.changedVehicleSpeed)

    def decelerate(self, decelerateRate, speedLimitedTo, vehicleSpeed):
        print("Decelerating..")
        print("Deceleration rate: ", self.decelerationRate)
        print("Speed limited to: ", speedLimitedTo)
        while vehicleSpeed > speedLimitedTo:
            time.sleep(decelerateRate)
            # convert to km/hr
            # if vehicleSpeed > speedLimitedTo:
            vehicleSpeed -= 1 * 3.6
            global changedVehicleSpeed
            self.changedVehicleSpeed = vehicleSpeed
            print("Speed: ", self.changedVehicleSpeed)

    @property
    def changedVehicleSpeed(self):
        # print("got speed changed")
        return self._changedVehicleSpeed

    @changedVehicleSpeed.setter
    def changedVehicleSpeed(self, new_value):
        # print("set changed speed")
        self._changedVehicleSpeed = new_value
        for callback in self._observers:
            callback(self._changedVehicleSpeed)

    def notifySpeedChange(self, callback):
        self._observers.append(callback)