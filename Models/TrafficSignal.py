import enum
import time


class TrafficSignalEnum(enum.Enum):
    Red = 2
    Green = 3
    Yellow = 1


currentSignal = "TrafficSignalEnum.Red"


class TrafficSignal:

    def oneRun(self):
        for signal in TrafficSignalEnum:
            print("Current signal: ", signal.name, " Wait time: ", signal.value)
            global currentSignal
            currentSignal = signal
            time.sleep(signal.value)
