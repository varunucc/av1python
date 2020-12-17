changedVehicleSpeed = 0


class SpeedControl:
    def __init__(self):
        self._speedObserver = []
        self._changedVehicleSpeed = 0
        self.accelerating = False
        self.rateOfAcceleration = 1

    def calculateAccelerationRateToLimitedSpeed(self, vehicleSpeed, speedLimitedTo):
        self.accelerate(self.rateOfAcceleration, speedLimitedTo, vehicleSpeed)

    def calculateDecelerationRateWithinDistance(self, vehicleSpeed, speedLimitedTo, distanceWithin):
        try:
            if distanceWithin > 0 and vehicleSpeed > 0:
                # formula: a = v v - u u / 2 s
                speedLimitedToInMetersPerSecond = speedLimitedTo / 3.6
                vehicleSpeedInMeterPerSecond = vehicleSpeed / 3.6
                rateOfDeceleration = (((speedLimitedToInMetersPerSecond ** 2) - (vehicleSpeedInMeterPerSecond ** 2)) / (
                            2 * distanceWithin))
                self.decelerate(rateOfDeceleration, speedLimitedTo, vehicleSpeed)
        except Exception as e:
            if distanceWithin < 0:
                raise ZeroDivisionError("distanceWithin was <= zero")
            elif vehicleSpeed < 0:
                raise ValueError("VehicleSpeed was <= 0")
            else:
                raise e

    def accelerate(self, rateOfAcceleration, speedLimitedTo, vehicleSpeed):
        # print("\nAccelerating..")
        # add in km/hr
        if rateOfAcceleration > 0:
            if vehicleSpeed < speedLimitedTo:
                vehicleSpeed += 3.6 * rateOfAcceleration
                if vehicleSpeed > speedLimitedTo:
                    vehicleSpeed = speedLimitedTo
            global changedVehicleSpeed
            self.changedVehicleSpeed = vehicleSpeed
        else:
            raise ValueError("acceleration rate was <=0")
        # print("\nSpeed from accelerating: ", self.changedVehicleSpeed)

    def decelerate(self, rateOfDeceleration, speedLimitedTo, vehicleSpeed):
        # print("\nDecelerating..")
        # subtract in km/hr
        if rateOfDeceleration < 0 and vehicleSpeed > 0:
            if vehicleSpeed > speedLimitedTo:
                vehicleSpeed += 3.6 * rateOfDeceleration
                if vehicleSpeed <= speedLimitedTo:
                    vehicleSpeed = speedLimitedTo
                global changedVehicleSpeed
                self.changedVehicleSpeed = vehicleSpeed
        else:
            raise ValueError("deceleration rate cannot be >= 0 or vehicle speed is <= 0")
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
