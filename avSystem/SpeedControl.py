changedVehicleSpeed = 0

rateOfDeceleration = 2.6


class SpeedControl:
    def __init__(self):
        self._speedObserver = []
        self._changedVehicleSpeed = 0
        self.accelerating = False
        self.rateOfAcceleration = 1

    def calculateAccelerationRateToLimitedSpeed(self, vehicleSpeed, speedLimitedTo):
        self.accelerate(self.rateOfAcceleration, speedLimitedTo, vehicleSpeed)

    def calculateDecelerationRateWithinDistance(self, vehicleSpeed, speedLimitedTo, distanceWithin):
        global rateOfDeceleration
        # formula: v v = u u + 2 a s
        speedLimitedToInMetersPerSecond = speedLimitedTo/3.6
        vehicleSpeedInMeterPerSecond = vehicleSpeed/3.6
        rateOfDeceleration = (((speedLimitedToInMetersPerSecond**2)-(vehicleSpeedInMeterPerSecond**2))/(2*distanceWithin))
        self.decelerate(rateOfDeceleration, speedLimitedTo, vehicleSpeed)

    def accelerate(self, accelerateRate, speedLimitedTo, vehicleSpeed):
        # print("\nAccelerating..")
        # add in km/hr
        if vehicleSpeed < speedLimitedTo:
            vehicleSpeed += 3.6 * accelerateRate
            if vehicleSpeed > speedLimitedTo:
                vehicleSpeed = speedLimitedTo
        global changedVehicleSpeed
        self.changedVehicleSpeed = vehicleSpeed
        # print("\nSpeed from accelerating: ", self.changedVehicleSpeed)

    def decelerate(self, decelerateRate, speedLimitedTo, vehicleSpeed):
        # print("\nDecelerating..")
        # subtract in km/hr
        if vehicleSpeed > speedLimitedTo:
            vehicleSpeed += 3.6 * decelerateRate
            if vehicleSpeed <= speedLimitedTo:
                vehicleSpeed = speedLimitedTo
            global changedVehicleSpeed
            self.changedVehicleSpeed = vehicleSpeed
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
