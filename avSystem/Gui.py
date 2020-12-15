import tkinter as tk

from Main import Main
from functools import partial


class Gui:
    def __init__(self):
        screen = tk.Tk()
        screen.geometry("350x250")
        screen.title("Autonomous VehicleV")
        tk.Label(text="Notes 1.0", bg="grey", width="300", height="2").pack()
        tk.Label(text="").pack()
        vehicleSpeedText = tk.Text(master=screen, width="300", height="2").pack()
        startButton = tk.Button(master=screen, text="Start", height="2", width="30",
                                command=partial(Main, vehicleSpeedText))
        # startButton.bind("<Button-1>", Main())
        startButton.pack()
        # tk.Button(text="Register").pack()
        screen.mainloop()
