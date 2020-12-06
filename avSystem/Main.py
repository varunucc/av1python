from avSystem.TrafficSignal import TrafficSignal
from avSystem.Car import Car
from avSystem.SpeedControl import SpeedControl
import concurrent.futures
import threading
import enum


class TrafficSignalEnum1(enum.Enum):
    Green = 3
    Yellow = 2
    Red = 1
    locationOnRoad = 120


class TrafficSignalEnum2(enum.Enum):
    Green = 1
    Yellow = 3
    Red = 2
    locationOnRoad = 220


signalList = [TrafficSignalEnum1, TrafficSignalEnum2]


class Main:

    def __init__(self):
        print("\nStarting traffic signal...")
        ts = TrafficSignal(signalList)
        sp = SpeedControl()
        trafficSignalThread = threading.Thread(target=ts.rotateSignals, daemon=True)
        trafficSignalThread.start()
        car = Car(ts, sp)
        trafficSignalThread.join()
        print("\nDone.")


def main():
    Main()


if __name__ == '__main__':
    main()

