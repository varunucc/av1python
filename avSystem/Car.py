import threading
import time

class Car(object):

    def __init__(self, ts, sp):

        self.vehicleSpeed = 0
        self.topSpeed = 60
        self.haltSpeed = 0
        self.slowDownSpeed = 20

        self.speedLimitedTo = self.haltSpeed
        self.trafficSignalColour = ''
        self.distanceToNextSignal = 0
        self.nextTrafficSignalLocationOnRoad = 0
        self.decelerationLock = False
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

        # declare threads
        self._speedMonitorThread = threading.Thread(target=self.speedMonitor, daemon=True)
        self._slowDownProgramThread = threading.Thread(target=self.speedControl.slowDownVehicleSpeed,
                                                       args=(self.vehicleSpeed, self.speedLimitedTo,
                                                             self.distanceToNextSignal,), daemon=True)
        self._haltProgramThread = threading.Thread(target=self.speedControl.bringVehicleToHalt,
                                                   args=(self.vehicleSpeed, self.speedLimitedTo,
                                                         self.distanceToNextSignal,), daemon=True)
        self._accelerateThread = threading.Thread(target=self.speedControl.calculateAccelerationRateToLimitedSpeed,
                                                  args=(self.vehicleSpeed, self.speedLimitedTo,), daemon=True)
        # Monitor speed and start accelerating
        self._monitorSpeed = True
        self.speedControl.accelerating = True
        self._speedMonitorThread.start()
        self._accelerateThread.start()
        self._accelerateThread.join()
        self._speedMonitorThread.join()

    def checkTrafficLightColour(self, signalColour):
        if signalColour.name == "Green":
            print("\nCar sees green signal")
            self.trafficSignalColour = signalColour.name
        elif signalColour.name == "Red":
            print("\nCar sees red signal")
            self.trafficSignalColour = signalColour.name
        elif signalColour.name == "Yellow":
            print("\nCar sees yellow signal")
            self.trafficSignalColour = signalColour.name

    def setRoadLengthCovered(self, speed):
        print("\nD")

    def setTrafficSignalLocation(self, distance):
        print("\nLocation of traffic signal on the road: {}mts".format(distance))
        self.nextTrafficSignalLocationOnRoad = distance

    def speedMonitor(self):
        while self._monitorSpeed:
            time.sleep(1.0)
            self.checkDistanceToTrafficSignal()
            self.actionAccordingToTrafficSignalColourAndDistance()

    def checkDistanceToTrafficSignal(self):
        # calculate road length covered
        self.roadLengthCovered += round(self.vehicleSpeed / 3.6)
        # print("\nRoad length covered: ", self.roadLengthCovered)

        # calculate distance to signal
        self.distanceToNextSignal = self.nextTrafficSignalLocationOnRoad - self.roadLengthCovered

        # next signal
        if self.distanceToNextSignal <= 0:
            self.distanceToNextSignal = 0
            self.trafficSignalData.nextSignal()

        print("\nDistance from signal: {}mts.".format(self.distanceToNextSignal))

    def setSpeedLimitedTo(self, speed):
        print("\nIncrementing speed.")

    def actionAccordingToTrafficSignalColourAndDistance(self):
        if 20 < self.distanceToNextSignal <= 80:
            if self.vehicleSpeed > 20:
                self.slowDown()
            else:
                print("\nMaintaining speed")
        if 0 < self.distanceToNextSignal <= 20:
            if self.trafficSignalColour == "Red":
                if self.vehicleSpeed > 0:
                    self.stopCar()
                else:
                    print("\nVehicle stopped")
                    # stop monitoring speed
                    self._monitorSpeed = False
                    # stop traffic signal
                    self.trafficSignalData.nextSignal()
            else:
                self._accelerateThread = threading.Thread(
                    target=self.speedControl.calculateAccelerationRateToLimitedSpeed,
                    args=(self.vehicleSpeed, self.speedLimitedTo,), daemon=True)
                self._accelerateThread.start()
        if self.distanceToNextSignal > 80:
            self.speedLimitedTo = self.topSpeed
            self._accelerateThread = threading.Thread(target=self.speedControl.calculateAccelerationRateToLimitedSpeed,
                                                      args=(self.vehicleSpeed, self.speedLimitedTo,), daemon=True)
            self._accelerateThread.start()

    def failureToReduceSpeedBefore20mtsCheck(self):
        print("\nReturn boolean")

    def setVehicleSpeed(self, speed):
        print("\nCurrent vehicle speed: {}km/hr".format(speed))
        self.vehicleSpeed = speed

    def slowDown(self):
        print("\nSlowing down")
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = self.slowDownSpeed
        self._slowDownProgramThread = threading.Thread(target=self.speedControl.slowDownVehicleSpeed,
                                                       args=(self.vehicleSpeed, self.speedLimitedTo,
                                                             self.distanceToNextSignal - 20,), daemon=True)
        self._slowDownProgramThread.start()

    def stopCar(self):
        print("\nStopping")
        self.speedControl.decelerating = False
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = self.haltSpeed
        self._haltProgramThread = threading.Thread(target=self.speedControl.bringVehicleToHalt,
                                                   args=(self.vehicleSpeed, self.speedLimitedTo,
                                                         self.distanceToNextSignal,), daemon=True)
        self._haltProgramThread.start()
