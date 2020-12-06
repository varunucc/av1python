from avSystem.TrafficSignal import TrafficSignal
import threading


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

        self._slowDownProgramThread = threading.Thread(target=self.speedControl.slowDownVehicleSpeed(
            self.vehicleSpeed, self.speedLimitedTo, self.distanceToNextSignal), daemon=True)
        self._haltProgramThread = threading.Thread(target=self.speedControl.bringVehicleToHalt(
            self.vehicleSpeed, self.speedLimitedTo, self.distanceToNextSignal), daemon=True)

        # Start accelerating
        self.speedControl.accelerating = True
        self._accelerateThread = threading.Thread(target=self.speedControl.calculateAccelerationRateToLimitedSpeed(
            self.vehicleSpeed, self.speedLimitedTo), daemon=True)
        self._accelerateThread.start()
        # self._accelerateThread.join()

    def checkTrafficLightColour(self, signalColour):
        if signalColour.name == "Green":
            print("Car sees green signal")
        elif signalColour.name == "Red":
            print("Car sees red signal")
        elif signalColour.name == "Yellow":
            print("Car sees yellow signal")
        self.trafficSignalColour = signalColour.name

    def setRoadLengthCovered(self, speed):
        print("D")

    def setTrafficSignalLocation(self, distance):
        print("Location of traffic signal: ", distance)
        self.nextTrafficSignalLocationOnRoad = distance

    def checkDistanceToTrafficSignal(self):
        self.distanceToNextSignal = self.nextTrafficSignalLocationOnRoad - self.roadLengthCovered

        # next signal
        if self.distanceToNextSignal <= 0:
            self.trafficSignalData.nextSignal()

        print("distance of signal: ", self.nextTrafficSignalLocationOnRoad)
        print("distance from signal: ", self.distanceToNextSignal)
        self.actionAccordingToTrafficSignalColourAndDistance()

    def setSpeedLimitedTo(self, speed):
        print("Incrementing speed.")

    def actionAccordingToTrafficSignalColourAndDistance(self):
        print("Action according called")
        if 20 < self.distanceToNextSignal <= 80:
            if (self._slowDownProgramThread is None) or (not self._slowDownProgramThread.is_alive()):
                self.slowDown()
        if 0 < self.distanceToNextSignal <= 20:
            if (self._haltProgramThread is None) or (not self._haltProgramThread.is_alive()):
                self.stopVehicle()



    def failureToReduceSpeedBefore20mtsCheck(self):
        print("Return boolean")

    def setVehicleSpeed(self, changedSpeed):
        self.vehicleSpeed = changedSpeed
        # calculate road length covered
        self.roadLengthCovered += float(changedSpeed / 3.6)

        print("Road length covered: ", self.roadLengthCovered)
        # adjusting distance to traffic signal
        self.checkDistanceToTrafficSignal()

        print("Speed of car: ", changedSpeed)

    def slowDown(self):
        print("Slowing down")
        self.speedControl.accelerating = False
        self.speedControl.slowDown = True
        self.speedLimitedTo = 20
        self._slowDownProgramThread.start()
        print("Slow down thread started")

    def stopVehicle(self):
        print("Stopping")
        self.speedControl.accelerating = False
        self.speedControl.slowDown = False
        self.speedControl.stop = True
        self.speedLimitedTo = 0
        self._haltProgramThread.start()
        print("Halt thread started")
