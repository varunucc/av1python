changedVehicleSpeed = 0

decelerationRate = 2.6


class SpeedControl:
    def __init__(self):
        self._speedObserver = []
        self._changedVehicleSpeed = 0
        self.accelerating = False
        self.accelerationRate = 1
        self.decelerateRateCalculated = False

    def calculateAccelerationRateToLimitedSpeed(self, vehicleSpeed, speedLimitedTo):
        self.accelerate(self.accelerationRate, speedLimitedTo, vehicleSpeed)

    def calculateDecelerationRateWithinDistance(self, vehicleSpeed, speedLimitedTo, distanceWithin):
        global decelerationRate
        # if not self.decelerateRateCalculated:
        # formula: v v = u u + 2 a s
        decelerationRate = ((((speedLimitedTo/3.6)**2)-((vehicleSpeed/3.6)**2))/(2*distanceWithin))
        self.decelerateRateCalculated = True
        # print("Vehicle speed: ", vehicleSpeed)
        # print("Distance within: ", distanceWithin)
        # print("Calculated deceleration rate: ", decelerationRate)
        self.decelerate(decelerationRate, speedLimitedTo, vehicleSpeed)

    def accelerate(self, accelerateRate, speedLimitedTo, vehicleSpeed):
        # print("\nAccelerating..")
        # convert to km/hr
        if vehicleSpeed < speedLimitedTo:
            vehicleSpeed += 3.6 * accelerateRate
            if vehicleSpeed > speedLimitedTo:
                vehicleSpeed = speedLimitedTo
        global changedVehicleSpeed
        self.changedVehicleSpeed = vehicleSpeed
        # print("\nSpeed from accelerating: ", self.changedVehicleSpeed)

    def decelerate(self, decelerateRate, speedLimitedTo, vehicleSpeed):
        # print("\nDecelerating..")
        # convert to km/hr
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
