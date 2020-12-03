from Models.TrafficSignal import TrafficSignal


class Car(object):

    def __init__(self, ts):
        self.data = ts
        self.data.signalChangeBroadcast(self.checkTrafficLightColour)

        self.vehicleSpeed = 0
        self.topSpeed = 120.0
        self.haltSpeed = 0.0
        self.speedLimitedTo = self.haltSpeed

        self.roadLengthCovered = 0
        self.distanceFromSignalToStartBreaking = 9999999
        self.failureModeEnabled = False


    def checkTrafficLightColour(self, signal):
        if signal.name == "Green":
            print("Car sees green signal")
        elif signal.name == "Red":
            print("Car sees red signal")
        elif signal.name == "Yellow":
            print("Car sees yellow signal")
        elif signal.name == "Distance":
            print("Distance :", signal.value)


    def checkDistanceToTrafficSignal(self):
        print("Distance remaining")

    def setSpeedLimitedTo(self, speed):
        print("Incrementing speed.")

    def actionAccordingToTrafficSignalColour(self, signal):
        print("Acting according to signal light")

    def failureToReduceSpeedBefore20mtsCheck(self):
        print("Return boolean")