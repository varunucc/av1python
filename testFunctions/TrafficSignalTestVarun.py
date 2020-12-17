import time
from mock import patch


# @patch('time.sleep', return_value=None)
def rotateSignals(signalCounter, trafficSignalList):
    # req Implement the traffic light color change.
    try:
        while signalCounter < len(trafficSignalList):
            currentSignal = trafficSignalList[signalCounter]
            for signalData in currentSignal:
                if signalData.name == "locationOnRoad":
                    continue
                print("\nCurrent traffic signal: {} Wait time: {}".format(signalData.name, signalData.value))
                # time.sleep(signalData.value)
                return signalData
    except Exception as e:
        return e


def goToNextSignalAndSetLocation(signalCounter, trafficSignalList):
    signalCounter += 1
    if signalCounter < len(trafficSignalList):
        return trafficSignalList[signalCounter]["locationOnRoad"].value
    return -1
