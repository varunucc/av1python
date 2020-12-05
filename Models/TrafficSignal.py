import time
import os

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

    def rotateSignals(self):
        while True:
            if not len(self.trafficSignalList) > 0:
                break
            for signals in self.trafficSignalList:
                global signalLocationOnRoad
                self.signalLocationOnRoad = signals["locationOnRoad"].value
                print("Been here")
                for signalLights in signals:
                    if signalLights.name == "locationOnRoad":
                        continue
                    print("Current traffic signal: ", signalLights.name, " Wait time: ", signalLights.value)
                    global currentSignalLight
                    self.currentSignalLight = signalLights
                    time.sleep(signalLights.value)

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

