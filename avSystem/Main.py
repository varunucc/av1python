from avSystem.TrafficSignal import TrafficSignal
from avSystem.Car import Car
from avSystem.SpeedControl import SpeedControl
import concurrent.futures
import threading
import enum


class TrafficSignalEnum1(enum.Enum):
    Green = 1
    Yellow = 3
    Red = 25
    locationOnRoad = 100


# Form signal list
signalList = [TrafficSignalEnum1]


class Main:

    def __init__(self):
        print("\nStarting traffic signals...")
        ts = TrafficSignal(signalList)
        sp = SpeedControl()
        trafficSignalThread = threading.Thread(target=ts.rotateSignals, daemon=True)
        trafficSignalThread.start()
        print("\nStarting car...")
        car = Car(ts, sp)
        trafficSignalThread.join()
        print("\nDone.")


def main():
    Main()


if __name__ == '__main__':
    main()

