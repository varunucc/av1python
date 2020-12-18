import threading
import time
import enum


class CarStatusEnums(enum.Enum):
    notMoving = "Not moving."
    maintainingSpeed = "Maintaining current speed..."
    accelerating = "Accelerating..."
    decelerating = "Slowing down..."
    stopping = "Stopping..."
    stopped = "Stopped."
    within80ButSpeedLessThan30 = "Speed less than 30, accelerating..."


vehicleSpeed = 0
distanceToNextSignal = 0
vehicleStatus = CarStatusEnums.notMoving


class Car(object):

    def __init__(self, ts, sp):
        global vehicleStatus
        self._vehicleStatus = CarStatusEnums.notMoving
        self._vehicleSpeed = 0

        # constant values
        self.topSpeed = 60
        self.haltSpeed = 0
        self.slowDownSpeed = 30

        self._speedObserver = []
        self._distanceObserver = []
        self._vehicleStatusObserver = []

        self.speedLimitedTo = self.haltSpeed
        self.trafficSignalColour = ''
        self._distanceToNextSignal = 0
        self.nextTrafficSignalLocationOnRoad = 0
        self._monitorSpeed = False

        self.roadLengthCovered = 0
        self.failureModeEnabled = False

        self.trafficSignalData = ts
        self.trafficSignalData.signalChangeBroadcast(self.checkTrafficLightColour)
        self.trafficSignalData.signalLocationBroadcast(self.setTrafficSignalLocation)
        self.nextTrafficSignalLocationOnRoad = self.trafficSignalData.signalLocationOnRoad

        # Bind changes from speed control
        self.speedControl = sp
        self.speedControl.notifySpeedChange(self.setVehicleSpeed)

        # declare thread
        self._speedMonitorThread = threading.Thread(target=self.speedAndDistanceToSignalMonitor, daemon=True)

        # Monitor speed and start accelerating
        self._monitorSpeed = True
        self.speedControl.accelerating = True
        self._speedMonitorThread.start()
        # self._speedMonitorThread.join()

    def checkTrafficLightColour(self, signalColour):
        # R2 req Make the car monitor the traffic light color change.
        if signalColour.name == "Green":
            print("\nCar sees green signal")
            self.trafficSignalColour = signalColour.name
        elif signalColour.name == "Red":
            print("\nCar sees red signal")
            self.trafficSignalColour = signalColour.name
        elif signalColour.name == "Yellow":
            print("\nCar sees yellow signal")
            self.trafficSignalColour = signalColour.name

    def setTrafficSignalLocation(self, distance):
        print("\nLocation of traffic signal on the road: {}mts".format(distance))
        self.nextTrafficSignalLocationOnRoad = distance

    def speedAndDistanceToSignalMonitor(self):
        # R6 req monitor vehicle speed distance to signal continuously
        while self._monitorSpeed:
            self.checkDistanceToTrafficSignal()
            self.actionAccordingToTrafficSignalColourAndDistance()
            time.sleep(1.0)

    def checkDistanceToTrafficSignal(self):
        global vehicleSpeed, distanceToNextSignal
        # calculate road length covered
        self.roadLengthCovered += (self.vehicleSpeed / 3.6)
        # print("\nRoad length covered: ", self.roadLengthCovered)

        # calculate distance to signal
        self.distanceToNextSignal = self.nextTrafficSignalLocationOnRoad - self.roadLengthCovered

        # next signal
        # print("Distance to signal: {}, vehicle speed: {}".format(self.distanceToNextSignal, self.vehicleSpeed))
        # R5 stop at exact location
        if self.distanceToNextSignal <= 0.1 and round(self.vehicleSpeed) <= 1:
            self.distanceToNextSignal = 0
            self.vehicleSpeed = 0
            self.trafficSignalData.goToNextSignalAndSetLocation()

        print("\nDistance from signal: {}mts".format(round(self.distanceToNextSignal, 2)))
        print("\nCurrent vehicle speed: {}km/hr".format(round(self.vehicleSpeed, 2)))

    def actionAccordingToTrafficSignalColourAndDistance(self):
        global vehicleSpeed, distanceToNextSignal, vehicleStatus
        # req Code the actions that the vehicle should perform according to the traffic light color + distance from
        # traffic light (Behavior System).
        # R1 req acc dec autonomously
        # R3 req Ensure that the vehicle slows down before the traffic light and stops
        # before the red traffic signal.
        if 20 < self.distanceToNextSignal <= 80:
            if self.vehicleSpeed < self.slowDownSpeed:
                print("\nAccelerating..")
                self.vehicleStatus = CarStatusEnums.within80ButSpeedLessThan30
                self.speedLimitedTo = self.slowDownSpeed
                self.speedControl.calculateAccelerationRateToLimitedSpeed(self.vehicleSpeed, self.speedLimitedTo)
            elif self.vehicleSpeed > self.slowDownSpeed:
                print("\nSlowing down")
                self.vehicleStatus = CarStatusEnums.decelerating
                self.slowDown()
            elif self.vehicleSpeed == self.slowDownSpeed:
                print("\nMaintaining speed")
                self.vehicleStatus = CarStatusEnums.maintainingSpeed
        elif 0 <= self.distanceToNextSignal <= 20:
            # R4 req stop vehicle at signal
            if self.trafficSignalColour == "Red" or self.trafficSignalColour == "Yellow":
                # print("Vehicle speed at stop car: ", self.vehicleSpeed)
                if self.vehicleSpeed > self.haltSpeed:
                    # print("Halt speed now at : ", (self._vehicleSpeed / 3.6))
                    print("\nStopping")
                    self.vehicleStatus = CarStatusEnums.stopping
                    self.stopCar()
                else:
                    print("\nVehicle stopped")
                    self.vehicleStatus = CarStatusEnums.stopped
                    # stop monitoring speed
                    self._monitorSpeed = False
                    # stop traffic signal
                    self.trafficSignalData.goToNextSignalAndSetLocation()
            else:
                print("\nAccelerating..")
                self.vehicleStatus = CarStatusEnums.accelerating
                self.speedLimitedTo = self.topSpeed
                self.speedControl.calculateAccelerationRateToLimitedSpeed(self.vehicleSpeed, self.speedLimitedTo)
        elif self.distanceToNextSignal > 80:
            # print("VEhicle speed: ", vehicleSpeed)
            if self.vehicleSpeed < self.topSpeed:
                print("\nAccelerating..")
                self.vehicleStatus = CarStatusEnums.accelerating
                self.speedLimitedTo = self.topSpeed
                self.speedControl.calculateAccelerationRateToLimitedSpeed(self.vehicleSpeed, self.speedLimitedTo)
            else:
                print("\nMaintaining speed")
                self.vehicleStatus = CarStatusEnums.maintainingSpeed


    def setVehicleSpeed(self, speed):
        global vehicleSpeed
        global distanceToNextSignal
        self.vehicleSpeed = speed

    def slowDown(self):
        global vehicleSpeed, distanceToNextSignal
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = self.slowDownSpeed
        self.speedControl.calculateDecelerationRateWithinDistance(self.vehicleSpeed, self.speedLimitedTo,
                                                                  self.distanceToNextSignal - 20)

    def stopCar(self):
        global vehicleSpeed, distanceToNextSignal
        self.speedControl.decelerating = False
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = self.haltSpeed
        self.speedControl.calculateDecelerationRateWithinDistance(self.vehicleSpeed, self.speedLimitedTo,
                                                                  self.distanceToNextSignal)

    @property
    def vehicleSpeed(self):
        return self._vehicleSpeed

    @vehicleSpeed.setter
    def vehicleSpeed(self, new_value):
        self._vehicleSpeed = new_value
        for callback in self._speedObserver:
            callback(self._vehicleSpeed)

    def speedToGui(self, callback):
        self._speedObserver.append(callback)

    @property
    def distanceToNextSignal(self):
        return self._distanceToNextSignal

    @distanceToNextSignal.setter
    def distanceToNextSignal(self, new_value):
        self._distanceToNextSignal = new_value
        for callback in self._distanceObserver:
            callback(self._distanceToNextSignal)

    def distanceToGui(self, callback):
        self._distanceObserver.append(callback)

    @property
    def vehicleStatus(self):
        return self._vehicleStatus

    @vehicleStatus.setter
    def vehicleStatus(self, new_value):
        self._vehicleStatus = new_value
        for callback in self._vehicleStatusObserver:
            callback(self._vehicleStatus)

    def vehicleStatusChange(self, callback):
        self._vehicleStatusObserver.append(callback)
