accelerateRate = 1.0
decelerationRate = 1.0


class SpeedControl:
    def __init__(self):
        print("SpeedControl")

    def slowDownVehicleSpeed(self, vehicleSpeed, speedLimitedTo):
        print("SlowDownVehicle")

    def bringVehicleToHalt(self, vehicleSpeed, speedLimitedTo):
        print("BringVehicleToHalt")

    def calculateAccelerationRateToLimitedSpeed(self, vehicleSpeed, speedLimitedTo):
        print("calculateAccelerationRateLimitedTo")

    def calculateDecelerationRateToLimitedSpeed(self, vehicleSpeed, speedLimitedTo):
        print("calculateDecelerationRateLimitedTo")

    def accelerate(self, accelerateRate, speedLimitedTo):
        print("Accelerate")

    def decelerate(self, decelerateRate, speedLimitedTo):
        print("Decelerate")
