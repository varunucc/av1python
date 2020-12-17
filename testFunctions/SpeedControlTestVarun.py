def calculateDecelerationRateWithinDistanceForTesting(vehicleSpeed, speedLimitedTo, distanceWithin):
    try:
        if distanceWithin > 0 and vehicleSpeed > 0:
            # formula: a = vv - u u / 2 s
            speedLimitedToInMetersPerSecond = speedLimitedTo / 3.6
            vehicleSpeedInMeterPerSecond = vehicleSpeed / 3.6
            return (((speedLimitedToInMetersPerSecond ** 2) - (vehicleSpeedInMeterPerSecond ** 2)) / (
                    2 * distanceWithin))
    except Exception as e:
        if distanceWithin < 0:
            raise ZeroDivisionError("distanceWithin was <= zero")
        elif vehicleSpeed < 0:
            raise ValueError("VehicleSpeed was <= 0")
        else:
            raise e


def accelerate(rateOfAcceleration, speedLimitedTo, vehicleSpeed):
    if rateOfAcceleration > 0:
        if vehicleSpeed < speedLimitedTo:
            vehicleSpeed += 3.6 * rateOfAcceleration
            if vehicleSpeed > speedLimitedTo:
                vehicleSpeed = speedLimitedTo
        return vehicleSpeed
    else:
        raise ValueError("acceleration rate was <=0")


def decelerate(rateOfDeceleration, speedLimitedTo, vehicleSpeed):
    if rateOfDeceleration < 0 and vehicleSpeed > 0:
        if vehicleSpeed > speedLimitedTo:
            vehicleSpeed += 3.6 * rateOfDeceleration
            if vehicleSpeed <= speedLimitedTo:
                vehicleSpeed = speedLimitedTo
        return vehicleSpeed
    else:
        raise ValueError("deceleration rate cannot be >= 0 or vehicle speed is <= 0")

