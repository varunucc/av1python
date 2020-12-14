from avSystem.TrafficSignal import TrafficSignal
from avSystem.Car import Car
from avSystem.SpeedControl import SpeedControl
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
        # print("")
        print("\nStarting traffic signals...")
        ts = TrafficSignal(signalList)
        sp = SpeedControl()
        trafficSignalThread = threading.Thread(target=ts.rotateSignals, daemon=True)
        trafficSignalThread.start()
        print("\nStarting car...")
        Car(ts, sp)
        trafficSignalThread.join()
        print("\nDone.")


def main():
    # screen = Tk()
    # screen.geometry("350x250")
    # screen.title("Autonomous VehicleV")
    # Label(text="Notes 1.0", bg="grey", width="300", height="2").pack()
    # Label(text="").pack()
    # Button(text="Login", height="2", width="30").pack()
    # Label(text="").pack()
    # Button(text="Register").pack()
    # screen.mainloop()
    Main()


if __name__ == '__main__':
    main()
