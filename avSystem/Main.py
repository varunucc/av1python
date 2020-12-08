from avSystem.TrafficSignal import TrafficSignal
from avSystem.Car import Car
from avSystem.SpeedControl import SpeedControl
import concurrent.futures
import threading
import enum


class TrafficSignalEnum1(enum.Enum):
    Green = 20
    Yellow = 4
    Red = 30
    locationOnRoad = 200


class TrafficSignalEnum2(enum.Enum):
    Green = 15
    Yellow = 4
    Red = 20
    locationOnRoad = 320


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

