import time

changedVehicleSpeed = 0


class SpeedControl:
    def __init__(self):
        self._speedObserver = []
        self._changedVehicleSpeed = 0
        self.accelerating = False
        self.accelerationRate = 1
        self.decelerationRate = 1
        self.brakeForce = 2.5

    def slowDownVehicleSpeed(self, vehicleSpeed, speedLimitedTo, distanceToSlowDownWithin):
        self.calculateDecelerationRateWithinDistance(vehicleSpeed, speedLimitedTo, distanceToSlowDownWithin)

    def bringVehicleToHalt(self, vehicleSpeed, speedLimitedTo, distanceToHaltWithin):
        self.calculateDecelerationRateWithinDistance(vehicleSpeed, speedLimitedTo, distanceToHaltWithin)

    def calculateAccelerationRateToLimitedSpeed(self, vehicleSpeed, speedLimitedTo):
        self.accelerate(self.accelerationRate, speedLimitedTo, vehicleSpeed)

    def calculateDecelerationRateWithinDistance(self, vehicleSpeed, speedLimitedTo, distanceWithin):
        # TODO calculate deceleration rate
        decelerationRate = 1
        # print("Vehicle speed: ", vehicleSpeed)
        # print("Distance within: ", distanceWithin)
        # print("Calculated deceleration rate: ", decelerationRate)
        self.decelerate(decelerationRate, speedLimitedTo, vehicleSpeed)

    def accelerate(self, accelerateRate, speedLimitedTo, vehicleSpeed):
        # print("\nAccelerating..")
        # convert to km/hr
        vehicleSpeed += 3.6
        if vehicleSpeed > speedLimitedTo:
            vehicleSpeed = speedLimitedTo
        global changedVehicleSpeed
        self.changedVehicleSpeed = round(vehicleSpeed)
        # print("\nSpeed from accelerating: ", self.changedVehicleSpeed)

    def decelerate(self, decelerateRate, speedLimitedTo, vehicleSpeed):
        # print("\nDecelerating..")
        # convert to km/hr
        vehicleSpeed -= (3.6 * self.brakeForce)
        if vehicleSpeed < speedLimitedTo:
            vehicleSpeed = speedLimitedTo
        global changedVehicleSpeed
        self.changedVehicleSpeed = round(vehicleSpeed)
        # print("\nSpeed from decelerating: ", self.changedVehicleSpeed)

    @property
    def changedVehicleSpeed(self):
        return self._changedVehicleSpeed

    @changedVehicleSpeed.setter
    def changedVehicleSpeed(self, new_value):
        self._changedVehicleSpeed = new_value
        for callback in self._speedObserver:
            callback(self._changedVehicleSpeed)

    def notifySpeedChange(self, callback):
        self._speedObserver.append(callback)
