from avSystem.TrafficSignal import TrafficSignal
import threading
import time

class Car(object):

    def __init__(self, ts, sp):
        self.vehicleSpeed = 0
        self.topSpeed = 60.0
        self.haltSpeed = 0.0
        self.speedLimitedTo = self.topSpeed
        self.trafficSignalColour = ''
        self.distanceToNextSignal = 0
        self.nextTrafficSignalLocationOnRoad = 0

        self.roadLengthCovered = 0
        self.distanceFromSignalToStartBreaking = 9999999
        self.failureModeEnabled = False

        self.trafficSignalData = ts
        self.trafficSignalData.signalChangeBroadcast(self.checkTrafficLightColour)
        self.trafficSignalData.signalLocationBroadcast(self.setTrafficSignalLocation)
        self.nextTrafficSignalLocationOnRoad = self.trafficSignalData.signalLocationOnRoad

        # Bind changes
        self.speedControl = sp
        self.speedControl.notifySpeedChange(self.setVehicleSpeed)

        # monitor speed
        self._speedMonitorThread = threading.Thread(target=self.speedMonitor, daemon=True)
        self._speedMonitorThread.start()

        self._slowDownProgramThread = threading.Thread(target=self.speedControl.slowDownVehicleSpeed,
                                                       args=(self.vehicleSpeed, self.speedLimitedTo,
                                                             self.distanceToNextSignal,), daemon=True)
        self._haltProgramThread = threading.Thread(target=self.speedControl.bringVehicleToHalt,
                                                   args=(self.vehicleSpeed, self.speedLimitedTo,
                                                         self.distanceToNextSignal,), daemon=True)

        # Start accelerating
        self.speedControl.accelerating = True
        self._accelerateThread = threading.Thread(target=self.speedControl.calculateAccelerationRateToLimitedSpeed,
                                                  args=(self.vehicleSpeed, self.speedLimitedTo,), daemon=True)
        self._accelerateThread.start()


    def checkTrafficLightColour(self, signalColour):
        if signalColour.name == "Green":
            print("\nCar sees green signal")
        elif signalColour.name == "Red":
            print("\nCar sees red signal")
        elif signalColour.name == "Yellow":
            print("\nCar sees yellow signal")
        self.trafficSignalColour = signalColour.name

    def setRoadLengthCovered(self, speed):
        print("\nD")

    def setTrafficSignalLocation(self, distance):
        print("\nLocation of traffic signal: ", distance)
        self.nextTrafficSignalLocationOnRoad = distance

    def checkDistanceToTrafficSignal(self):
        self.distanceToNextSignal = self.nextTrafficSignalLocationOnRoad - self.roadLengthCovered

        # next signal
        if self.distanceToNextSignal <= 0:
            self.trafficSignalData.nextSignal()

        print("\ndistance of signal: ", self.nextTrafficSignalLocationOnRoad)
        print("\ndistance from signal: ", self.distanceToNextSignal)

    def setSpeedLimitedTo(self, speed):
        print("\nIncrementing speed.")

    def actionAccordingToTrafficSignalColourAndDistance(self):
        # print("\nAction according called")
        if self.vehicleSpeed > 0 or self.distanceToNextSignal > 0:
            if 20 < self.distanceToNextSignal <= 80:
                if not self._slowDownProgramThread.is_alive():
                    self.slowDown()
            if 0 < self.distanceToNextSignal <= 20:
                if not self._haltProgramThread.is_alive():
                    self.stopCar()

    def failureToReduceSpeedBefore20mtsCheck(self):
        print("\nReturn boolean")

    def setVehicleSpeed(self, speed):
        self.vehicleSpeed = speed
        # calculate road length covered
        self.roadLengthCovered += speed / 3.6

        print("\nRoad length covered: ", self.roadLengthCovered)
        # adjusting distance to traffic signal
        self.checkDistanceToTrafficSignal()

        print("\nCurrent speed of car: ", speed)

    def slowDown(self):
        print("\nSlowing down")
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = 20
        self._slowDownProgramThread = threading.Thread(target=self.speedControl.slowDownVehicleSpeed,
                                                       args=(self.vehicleSpeed, self.speedLimitedTo,
                                                             self.distanceToNextSignal,), daemon=True)
        self._slowDownProgramThread.start()
        # self._slowDownProgramThread.join()

    def stopCar(self):
        print("\nStopping")
        self.speedControl.decelerating = False
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = 0
        self._haltProgramThread = threading.Thread(target=self.speedControl.bringVehicleToHalt,
                                                   args=(self.vehicleSpeed, self.speedLimitedTo,
                                                         self.distanceToNextSignal,), daemon=True)
        self._haltProgramThread.start()
        # self._haltProgramThread.join()
        print("\nHalt thread started")

    def speedMonitor(self):
        while True:
            time.sleep(1)
            self.setVehicleSpeed(speed=self.vehicleSpeed)
            self.actionAccordingToTrafficSignalColourAndDistance()
