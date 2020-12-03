import time
import os

trafficSignalList = []
currentSignal = ''
signalLocationOnRoad = 0


class TrafficSignal(object):
    def __init__(self, trafficSignals):
        global trafficSignalList
        self._observersTrafficLight = []
        self._observersTrafficSignalLocation = []
        self._currentSignal = ''
        self._signalLocationOnRoad = ''
        self.trafficSignalList = trafficSignals

    def rotateSignals(self):
        while True:
            if not len(self.trafficSignalList) > 0:
                break
            for signals in self.trafficSignalList:
                global currentSignal
                for signalLights in signals:
                    if signalLights.name == "locationOnRoad":
                        global signalLocationOnRoad
                        self.signalLocationOnRoad = signalLights.value
                    print("Current traffic signal: ", signalLights.name, " Wait time: ", signalLights.value)
                    global currentSignal
                    self.currentSignal = signalLights
                    time.sleep(signalLights.value)

    @property
    def currentSignal(self):
        return self._currentSignal

    @currentSignal.setter
    def currentSignal(self, new_value):
        self._currentSignal = new_value
        for callback in self._observersTrafficLight:
            callback(self._currentSignal)

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

