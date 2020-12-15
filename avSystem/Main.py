from avSystem.TrafficSignal import TrafficSignal
from avSystem.Car import Car
from avSystem.SpeedControl import SpeedControl
import threading
from tkinter import *
import time
import enum


class TrafficSignalEnum1(enum.Enum):
    Green = 1
    Yellow = 3
    Red = 25
    locationOnRoad = 99


# Form signal list
signalList = [TrafficSignalEnum1]


class Main:

    def __init__(self):
        self.currentVehicleSpeed = 0
        global signalList
        self.currentDistanceToSignal = signalList[0]["locationOnRoad"].value
        self.guiScreen = Tk()
        self.guiScreen.geometry("350x250")
        self.guiScreen.title("Autonomous VehicleV")
        # tk.Label(text="Notes 1.0", bg="grey", width="300", height="2").pack()
        Label(text="").pack()
        self.vehicleSpeedGui = Label(master=self.guiScreen, text=self.currentVehicleSpeed, width="300", height="2")
        self.vehicleSpeedGui.pack()
        self.distanceToSignalGui = Label(master=self.guiScreen, text=self.currentDistanceToSignal, width="300", height="2")
        self.distanceToSignalGui.pack()
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
        # sp.notifySpeedChange(self.updateSpeed)
        trafficSignalThread = threading.Thread(target=ts.rotateSignals, daemon=True)
        trafficSignalThread.start()
        print("\nStarting car...")
        car = Car(ts, sp)
        car.speedToGui(self.updateSpeed)
        car.distanceToGui(self.updateDistance)
        # trafficSignalThread.join()
        # print("\nDone.")

    def updateSpeed(self, speed):
        # print("Called update speed: ", speed)
        self.vehicleSpeedGui.config(text=speed)
        # self.guiScreen.update()

    def updateDistance(self, distance):
        # print("Called update speed: ", speed)
        self.distanceToSignalGui.config(text=distance)
        # self.guiScreen.update()

    def showGui(self):
        # self.guiScreen.after(1000, self.updateValues)
        self.guiScreen.mainloop()



def main():
    Main()


if __name__ == '__main__':
    main()
