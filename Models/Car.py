from Models.TrafficSignal import TrafficSignal


class Car(object):

    def __init__(self, ts):
        self.data = ts
        self.data.signalChangeBroadcast(self.checkTrafficLightColour)

        self.vehicleSpeed = 0
        self.topSpeed = 120
        self.speedLimitedTo = 0

        self.accelerationRate = 1
        self.decelerationRate = 0.5

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

        self.actionAccordingToTrafficSignalColour(signal)

    def checkDistanceToTrafficSignal(self):
        print("Distance remaining")

    def setSpeedLimitedTo(self, speed):
        print("Incrementing speed.")

    def actionAccordingToTrafficSignalColour(self, signal):
        print("Acting according to signal light")

    def failureToReduceSpeedBefore20mtsCheck(self):
        print("Return boolean")