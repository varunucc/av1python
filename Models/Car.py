from Models.TrafficSignal import TrafficSignal
import threading

distanceToNextSignal = 9999999
nextTrafficSignalLocationOnRoad = 0

class Car(object):

    def __init__(self, ts, sp):
        self.vehicleSpeed = 0
        self.topSpeed = 20.0
        self.haltSpeed = 0.0
        self.speedLimitedTo = self.topSpeed

        self.roadLengthCovered = 0
        self.distanceFromSignalToStartBreaking = 9999999
        self.failureModeEnabled = False

        self.trafficSignalData = ts
        self.trafficSignalData.signalChangeBroadcast(self.checkTrafficLightColour)
        self.trafficSignalData.signalLocationBroadcast(self.setTrafficSignalLocation)
        global nextTrafficSignalLocationOnRoad
        nextTrafficSignalLocationOnRoad = self.trafficSignalData.currentSignalDistance

        # Bind changes
        self.speedControl = sp
        self.speedControl.notifySpeedChange(self.setVehicleSpeed)

        # Start accelerating
        self._accelerateThread = threading.Thread(target=self.speedControl.calculateAccelerationRateToLimitedSpeed(
            self.vehicleSpeed, self.speedLimitedTo), daemon=True)
        self._accelerateThread.start()
        # self._accelerateThread.join()


    def checkTrafficLightColour(self, signal):
        if signal.name == "Green":
            print("Car sees green signal")
        elif signal.name == "Red":
            print("Car sees red signal")
        elif signal.name == "Yellow":
            print("Car sees yellow signal")


    def setRoadLengthCovered(self, speed):
        print("D")


    def setTrafficSignalLocation(self, distance):
        print("Location of traffic signal: ", distance)
        global nextTrafficSignalLocationOnRoad
        nextTrafficSignalLocationOnRoad = distance

    def checkDistanceToTrafficSignal(self):
        global distanceToNextSignal, nextTrafficSignalLocationOnRoad
        distanceToNextSignal = nextTrafficSignalLocationOnRoad - self.roadLengthCovered
        print("distance of signal: ", nextTrafficSignalLocationOnRoad)
        print("distance from signal: ", distanceToNextSignal)


    def setSpeedLimitedTo(self, speed):
        print("Incrementing speed.")

    def actionAccordingToTrafficSignalColour(self, signal):
        print("Acting according to signal light")

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
