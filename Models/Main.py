from Models.TrafficSignal import TrafficSignal
from Models.Car import Car
from Models.SpeedControl import SpeedControl
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
    locationOnRoad = 200


signalList = [TrafficSignalEnum1, TrafficSignalEnum2]


class Main:

    def __init__(self):
        print("Starting traffic signal...")
        ts = TrafficSignal(signalList)
        sp = SpeedControl()
        trafficSignalThread = threading.Thread(target=ts.rotateSignals, daemon=True)
        trafficSignalThread.start()
        car = Car(ts, sp)
        trafficSignalThread.join()
        print("Done.")


def main():
    Main()


if __name__ == '__main__':
    main()

