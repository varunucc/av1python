from avSystem.TrafficSignal import TrafficSignal
from avSystem.Car import Car
from avSystem.SpeedControl import SpeedControl
import threading
from tkinter import *
import time
import enum


class TrafficSignalEnum1(enum.Enum):
    Green = 2
    Yellow = 3
    Red = 25
    locationOnRoad = 120


# Form signal list
signalList = [TrafficSignalEnum1]


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
        self.vehicleSpeedGui = Label(master=self.guiScreen, text= self.currentVehicleSpeedText.format(self.currentVehicleSpeed), width="300", height="2")
        self.vehicleSpeedGui.pack()
        self.distanceToSignalGui = Label(master=self.guiScreen, text= self.distanceToSignalText.format(self.currentDistanceToSignal), width="300", height="2")
        self.distanceToSignalGui.pack()
        self.locationOfSignalGui = Label(master=self.guiScreen, text= self.locationOfSignalText.format(self.currentDistanceToSignal), width="300",
                                         height="2")
        self.locationOfSignalGui.pack()
        self.signalColourGui = Label(master=self.guiScreen, text= self.trafficSignalColourText.format("Start to know"), width="300",
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
        # trafficSignalThread.join()
        # print("\nDone.")

    def updateSpeed(self, speed):
        self.vehicleSpeedGui.config(text=self.currentVehicleSpeedText.format(round(speed, 2)))

    def updateDistanceToSignal(self, distance):
        self.distanceToSignalGui.config(text=self.distanceToSignalText.format(round(distance, 2)))

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
