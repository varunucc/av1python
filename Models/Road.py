from Models.TrafficSignal import TrafficSignal
from Models.Car import Car
import concurrent.futures
import threading
import enum


class TrafficSignalEnum1(enum.Enum):
    Green = 3
    Yellow = 6
    Red = 7
    Distance = 110


signalList = [TrafficSignalEnum1, TrafficSignalEnum1, TrafficSignalEnum1]


class Road:

    def __init__(self):
        print("Starting traffic signal...")
        ts = TrafficSignal(signalList)
        Car(ts)
        trafficSignalThread = threading.Thread(target=ts.rotateSignals, daemon=True)
        trafficSignalThread.start()
        trafficSignalThread.join(10000)
        print("Done.")


def main():
    Road()


if __name__ == '__main__':
    main()

