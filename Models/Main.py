from Models.TrafficSignal import TrafficSignal
from Models.Car import Car
import concurrent.futures
import threading
import enum


class TrafficSignalEnum1(enum.Enum):
    Green = 3
    Yellow = 2
    Red = 1
    locationOnRoad = 4


signalList = [TrafficSignalEnum1, TrafficSignalEnum1]


class Main:

    def __init__(self):
        print("Starting traffic signal...")
        ts = TrafficSignal(signalList)
        Car(ts)
        trafficSignalThread = threading.Thread(target=ts.rotateSignals, daemon=True)
        trafficSignalThread.start()
        trafficSignalThread.join(10)
        print("Done.")


def main():
    Main()


if __name__ == '__main__':
    main()

