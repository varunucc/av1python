from avSystem.TrafficSignal import TrafficSignal
from avSystem.Car import Car
from avSystem.SpeedControl import SpeedControl
import threading
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import enum


class TrafficSignalEnum(enum.Enum):
    Green = 19
    Yellow = 2
    Red = 1
    locationOnRoad = 100


signalList = [TrafficSignalEnum]

# graph
speedDistanceGraph = plt.figure()
ax1 = speedDistanceGraph.add_subplot(1, 1, 1)
vehicleSpeedArray = [0]
distanceToSignalArray = [0]


class Main:

    def __init__(self):
        self.currentVehicleSpeed = 0
        global signalList
        self.currentDistanceToSignal = signalList[0]["locationOnRoad"].value

        # text constants
        self.trafficSignalColourText = "Traffic signal colour: {}"
        self.distanceToSignalText = "Distance to signal: {}"
        self.currentVehicleSpeedText = "Current vehicle speed: {}"
        self.locationOfSignalText = "Location of signal: {}"
        self.vehicleStatusText = "Vehicle status: {}"

        self.guiScreen = Tk()
        self.guiScreen.geometry("350x250")
        self.guiScreen.title("Autonomous VehicleV")
        # tk.Label(text="Notes 1.0", bg="grey", width="300", height="2").pack()
        Label(text="").pack()
        self.vehicleSpeedGui = Label(master=self.guiScreen,
                                     text=self.currentVehicleSpeedText.format(self.currentVehicleSpeed), width="300",
                                     height="2")
        self.vehicleSpeedGui.pack()
        self.distanceToSignalGui = Label(master=self.guiScreen,
                                         text=self.distanceToSignalText.format(self.currentDistanceToSignal),
                                         width="300", height="2")
        self.distanceToSignalGui.pack()
        self.locationOfSignalGui = Label(master=self.guiScreen,
                                         text=self.locationOfSignalText.format(self.currentDistanceToSignal),
                                         width="300",
                                         height="2")
        self.locationOfSignalGui.pack()
        self.signalColourGui = Label(master=self.guiScreen, text=self.trafficSignalColourText.format("Start to know"),
                                     width="300",
                                     height="2")
        self.signalColourGui.pack()
        self.vehicleStatusGui = Label(master=self.guiScreen, text=self.vehicleStatusText.format("Stopped."),
                                      width="300",
                                      height="2")
        self.vehicleStatusGui.pack()
        self.startButton = Button(master=self.guiScreen, text="Start", height="2", width="30",
                                  command=self.startProgram)
        # startButton.bind("<Button-1>", Main())
        self.startButton.pack()
        # tk.Button(text="Register").pack()
        self.showGui()

    def startProgram(self):
        # print("")
        print("\nStarting traffic signals...")
        ts = TrafficSignal(signalList)
        sp = SpeedControl()
        ts.signalLocationBroadcast(self.updateSignalLocation)
        ts.signalChangeBroadcast(self.updateSignalColor)
        trafficSignalThread = threading.Thread(target=ts.rotateSignals, daemon=True)
        trafficSignalThread.start()
        print("\nStarting car...")
        car = Car(ts, sp)
        car.speedToGui(self.updateSpeed)
        car.distanceToGui(self.updateDistanceToSignal)
        car.vehicleStatusChange(self.updateVehicleStatus)
        self.showGraph()
        # trafficSignalThread.join()
        # print("\nDone.")

    def updateGraph(self, i):
        global speedDistanceGraph, ax1, vehicleSpeedArray, distanceToSignalArray
        ax1.clear()
        ax1.plot(distanceToSignalArray, vehicleSpeedArray, '-r')
        plt.xlabel("Distance covered (mts)")
        plt.ylabel("Vehicle speed (km/hr)")
        plt.title("Signal located at {}mts".format(self.currentDistanceToSignal))

    def showGraph(self):
        ani = FuncAnimation(speedDistanceGraph, self.updateGraph, interval=1000)
        plt.show()

    def updateSpeed(self, speed):
        global vehicleSpeedArray, distanceToSignalArray
        # print("length speed: ", len(vehicleSpeedArray))
        vehicleSpeedArray.append(round(speed, 2))
        distanceToSignalArray.append(distanceToSignalArray[len(distanceToSignalArray)-1])
        try:
            self.vehicleSpeedGui.config(text=self.currentVehicleSpeedText.format(round(speed, 2)))
        except Exception as e:
            print(e)

    def updateDistanceToSignal(self, distance):
        # TODO
        # if distanceToSignalArray == 0:
        #     ani.event_source.

        # handle negative distance
        global distanceToSignalArray, vehicleSpeedArray
        # print("length distance: ", len(distanceToSignalArray))
        vehicleSpeedArray.append(vehicleSpeedArray[len(vehicleSpeedArray)-1])
        distanceToSignalArray.append(round((self.currentDistanceToSignal - distance), 2))
        try:
            self.distanceToSignalGui.config(text=self.distanceToSignalText.format(round(distance, 2)))
        except Exception as e:
            print(e)

    def updateSignalColor(self, colour):
        self.signalColourGui.config(text=self.trafficSignalColourText.format(colour.name))

    def updateSignalLocation(self, locationOfSignal):
        self.distanceToSignalGui.config(text=self.locationOfSignalText.format(locationOfSignal))

    def updateVehicleStatus(self, status):
        self.vehicleStatusGui.config(text=self.vehicleStatusText.format(status.value))

    def showGui(self):
        self.guiScreen.mainloop()


def main():
    Main()


if __name__ == '__main__':
    main()
