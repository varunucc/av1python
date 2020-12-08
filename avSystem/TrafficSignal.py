import time

trafficSignalList = []
currentSignalLight = ''
signalLocationOnRoad = 0


class TrafficSignal(object):
    def __init__(self, trafficSignals):
        self._observersTrafficLight = []
        self._observersTrafficSignalLocation = []
        self._currentSignalLight = ''
        self._signalLocationOnRoad = ''
        self.currentSignalDistance = 0
        global trafficSignalList
        self.trafficSignalList = trafficSignals
        self.signalCounter = 0

        # assign distance of first signal
        global signalLocationOnRoad
        self.signalLocationOnRoad = self.trafficSignalList[0]["locationOnRoad"].value

    def rotateSignals(self):
        while self.signalCounter < len(self.trafficSignalList):
            currentSignal = self.trafficSignalList[self.signalCounter]
            # print("\nBeen here")
            for signalData in currentSignal:
                if signalData.name == "locationOnRoad":
                    continue
                print("\nCurrent traffic signal: {} Wait time: {}".format(signalData.name, signalData.value))
                global currentSignalLight
                self.currentSignalLight = signalData
                time.sleep(signalData.value)

    def nextSignal(self):
        # print("\nNext signal called")
        self.signalCounter += 1
        if self.signalCounter < len(self.trafficSignalList):
            # assign distance to signal
            global signalLocationOnRoad
            self.signalLocationOnRoad = self.trafficSignalList[self.signalCounter]["locationOnRoad"].value

    @property
    def currentSignalLight(self):
        return self._currentSignalLight

    @currentSignalLight.setter
    def currentSignalLight(self, new_value):
        self._currentSignalLight = new_value
        for callback in self._observersTrafficLight:
            callback(self._currentSignalLight)

    def signalChangeBroadcast(self, callback):
        self._observersTrafficLight.append(callback)

    @property
    def signalLocationOnRoad(self):
        return self._signalLocationOnRoad

    @signalLocationOnRoad.setter
    def signalLocationOnRoad(self, new_value):
        self._signalLocationOnRoad = new_value
        for callback in self._observersTrafficSignalLocation:
            callback(self._signalLocationOnRoad)

    def signalLocationBroadcast(self, callback):
        self._observersTrafficSignalLocation.append(callback)

