from Models.TrafficSignal import TrafficSignal
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

        # Start accelerating
        self.speedControl.accelerating = True
        self.accelerateThread = threading.Thread(target=self.speedControl.calculateAccelerationRateToLimitedSpeed(
            self.vehicleSpeed, self.speedLimitedTo), daemon=True)
        self.accelerateThread.start()
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
        print("distance of signal: ", self.nextTrafficSignalLocationOnRoad)
        print("distance from signal: ", self.distanceToNextSignal)
        self.actionAccordingToTrafficSignalColourAndDistance()


    def setSpeedLimitedTo(self, speed):
        print("Incrementing speed.")

    def actionAccordingToTrafficSignalColourAndDistance(self):
        print("Action according called")
        if self.distanceToNextSignal <= 0:
            self.trafficSignalData.nextSignal()
        if 20 < self.distanceToNextSignal <= 80:
            print("Slowing down")
            self.speedControl.accelerating = False
            self.speedControl.slowDown = True
            self.speedLimitedTo = 20
            slowDownProgramThread = threading.Thread(target=self.speedControl.slowDownVehicleSpeed(
                self.vehicleSpeed, self.speedLimitedTo, self.distanceToNextSignal), daemon=True)
            slowDownProgramThread.start()
        if 0 < self.distanceToNextSignal <= 20:
            print("Stopping")
            self.speedControl.accelerating = False
            self.speedControl.slowDown = False
            self.speedControl.stop = True
            self.speedLimitedTo = 0
            haltProgramThread = threading.Thread(target=self.speedControl.bringVehicleToHalt(
                self.vehicleSpeed, self.speedLimitedTo, self.distanceToNextSignal), daemon=True)
            haltProgramThread.start()

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
