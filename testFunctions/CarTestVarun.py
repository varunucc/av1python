from avSystem.Car import CarStatusEnums

topSpeed = 60
slowDownSpeed = 30
haltSpeed = 0
vehicleStatus = CarStatusEnums.notMoving


def actionAccordingToTrafficSignalColourAndDistance(vehicleSpeed, distanceToNextSignal, trafficSignalColour):
    # req Code the actions that the vehicle should perform according to the traffic light color + distance from
    # traffic light (Behavior System).
    # req Ensure that the vehicle slows down before the traffic light and stops
    # before the red traffic signal.
    global topSpeed, slowDownSpeed, haltSpeed, vehicleStatus
    if 20 < distanceToNextSignal <= 80:
        if vehicleSpeed < slowDownSpeed:
            print("\nAccelerating..")
            vehicleStatus = CarStatusEnums.within80ButSpeedLessThan30
            speedLimitedTo = slowDownSpeed
        elif vehicleSpeed > slowDownSpeed:
            print("\nSlowing down")
            vehicleStatus = CarStatusEnums.decelerating
        elif vehicleSpeed == slowDownSpeed:
            print("\nMaintaining speed")
            vehicleStatus = CarStatusEnums.maintainingSpeed
    elif 0 <= distanceToNextSignal <= 20:
        if trafficSignalColour == "Red" or trafficSignalColour == "Yellow":
            # print("Vehicle speed at stop car: ", vehicleSpeed)
            if vehicleSpeed > haltSpeed:
                # print("Halt speed now at : ", (_vehicleSpeed / 3.6))
                print("\nStopping")
                vehicleStatus = CarStatusEnums.stopping
            else:
                print("\nVehicle stopped")
                vehicleStatus = CarStatusEnums.stopped
                # stop monitoring speed
                _monitorSpeed = False
                # stop traffic signal
        else:
            print("\nAccelerating..")
            vehicleStatus = CarStatusEnums.accelerating
            speedLimitedTo = topSpeed
    elif distanceToNextSignal > 80:
        if vehicleSpeed < topSpeed:
            print("\nAccelerating..")
            vehicleStatus = CarStatusEnums.accelerating
            speedLimitedTo = topSpeed
        else:
            print("\nMaintaining speed")
            vehicleStatus = CarStatusEnums.maintainingSpeed
    return vehicleStatus
