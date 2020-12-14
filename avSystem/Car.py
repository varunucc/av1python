import threading
import time


class Car(object):

    def __init__(self, ts, sp):

        self.vehicleSpeed = 0
        self.topSpeed = 60
        self.haltSpeed = 0
        self.slowDownSpeed = 30

        self.speedLimitedTo = self.haltSpeed
        self.trafficSignalColour = ''
        self.distanceToNextSignal = 0
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
        self._speedMonitorThread.join()

    def checkTrafficLightColour(self, signalColour):
        # req Make the car monitor the traffic light color change.
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
        while self._monitorSpeed:
            self.checkDistanceToTrafficSignal()
            self.actionAccordingToTrafficSignalColourAndDistance()
            time.sleep(1.0)

    def checkDistanceToTrafficSignal(self):
        # calculate road length covered
        self.roadLengthCovered += (self.vehicleSpeed / 3.6)
        # print("\nRoad length covered: ", self.roadLengthCovered)

        # calculate distance to signal
        self.distanceToNextSignal = self.nextTrafficSignalLocationOnRoad - self.roadLengthCovered

        # next signal
        # print("Distance to signal: {}, vehicle speed: {}".format(self.distanceToNextSignal, self.vehicleSpeed))
        if self.distanceToNextSignal <= 0.1 and round(self.vehicleSpeed) <= 1:
            self.distanceToNextSignal = 0
            self.vehicleSpeed = 0
            self.trafficSignalData.nextSignal()

        print("\nDistance from signal: {}mts".format(round(self.distanceToNextSignal, 2)))
        print("\nCurrent vehicle speed: {}km/hr".format(round(self.vehicleSpeed, 2)))

    def actionAccordingToTrafficSignalColourAndDistance(self):
        # req Code the actions that the vehicle should perform according to the traffic light color + distance from
        # traffic light (Behavior System).
        # req Ensure that the vehicle slows down before the traffic light and stops
        # before the red traffic signal.
        if 20 < self.distanceToNextSignal <= 80:
            if self.vehicleSpeed > self.slowDownSpeed:
                self.slowDown()
            else:
                print("\nMaintaining speed")
        elif 0 <= self.distanceToNextSignal <= 20:
            if self.trafficSignalColour == "Red":
                # print("Vehicle speed at stop car: ", self.vehicleSpeed)
                if self.vehicleSpeed > self.haltSpeed:
                    # print("Halt speed now at : ", (self.vehicleSpeed / 3.6))
                    self.stopCar()
                else:
                    print("\nVehicle stopped")
                    # stop monitoring speed
                    self._monitorSpeed = False
                    # stop traffic signal
                    self.trafficSignalData.nextSignal()
            else:
                self.speedControl.calculateAccelerationRateToLimitedSpeed(self.vehicleSpeed, self.speedLimitedTo)
        elif self.distanceToNextSignal > 80:
            self.speedLimitedTo = self.topSpeed
            self.speedControl.calculateAccelerationRateToLimitedSpeed(self.vehicleSpeed, self.speedLimitedTo)
        else:
            raise ValueError("Minimum distance from signal should be > 80mts.")

    def setVehicleSpeed(self, speed):
        self.vehicleSpeed = speed

    def slowDown(self):
        print("\nSlowing down")
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = self.slowDownSpeed
        self.speedControl.calculateDecelerationRateWithinDistance(self.vehicleSpeed, self.speedLimitedTo,
                                                                  self.distanceToNextSignal - 20)

    def stopCar(self):
        print("\nStopping")
        self.speedControl.decelerating = False
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = self.haltSpeed
        self.speedControl.calculateDecelerationRateWithinDistance(self.vehicleSpeed, self.speedLimitedTo,
                                                                  self.distanceToNextSignal)
