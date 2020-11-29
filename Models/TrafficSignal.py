import time
import os

trafficSignalList = []
currentSignal = ''


class TrafficSignal(object):
    def __init__(self, trafficSignals):
        global trafficSignalList
        self._observers = []
        self._currentSignal = ''
        self.trafficSignalList = trafficSignals

    def rotateSignals(self):
        while True:
            if not len(self.trafficSignalList) > 0:
                break
            for signals in self.trafficSignalList:
                for signalLights in signals:
                    if signalLights.name == "Distance":
                        continue
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
        for callback in self._observers:
            callback(self._currentSignal)

    def signalChangeBroadcast(self, callback):
        self._observers.append(callback)

