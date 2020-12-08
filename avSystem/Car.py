from avSystem.TrafficSignal import TrafficSignal
import threading
import concurrent.futures
import time

class Car(object):

    def __init__(self, ts, sp):

        self.vehicleSpeed = 0
        self.topSpeed = 60.0
        self.haltSpeed = 0.0
        self.speedLimitedTo = self.topSpeed
        self.trafficSignalColour = ''
        self.distanceToNextSignal = 0
        self.nextTrafficSignalLocationOnRoad = 0
        self.decelerationLock = False
        self._monitorSpeed = False

        self.roadLengthCovered = 0
        self.distanceFromSignalToStartBreaking = 9999999
        self.failureModeEnabled = False

        self.trafficSignalData = ts
        self.trafficSignalData.signalChangeBroadcast(self.checkTrafficLightColour)
        self.trafficSignalData.signalLocationBroadcast(self.setTrafficSignalLocation)
        self.nextTrafficSignalLocationOnRoad = self.trafficSignalData.signalLocationOnRoad

        # Bind changes
        self.speedControl = sp
        self.speedControl.notifySpeedChange(self.setVehicleSpeed)
        self.speedControl.notifyDecelerationLock(self.setDecelerationLock)

        # monitor speed
        self._speedMonitorThread = threading.Thread(target=self.speedMonitor, daemon=True)

        self._slowDownProgramThread = threading.Thread(target=self.speedControl.slowDownVehicleSpeed,
                                                 args=(self.vehicleSpeed, self.speedLimitedTo,
                                                       self.distanceToNextSignal,), daemon=True)
        self._haltProgramThread = threading.Thread(target=self.speedControl.bringVehicleToHalt,
                                             args=(self.vehicleSpeed, self.speedLimitedTo,
                                                   self.distanceToNextSignal,), daemon=True)

        self.speedControl.accelerating = True
        # self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        # self._accelerateThread = threading.Thread(target=self.speedControl.calculateAccelerationRateToLimitedSpeed,
        #                                           args=(self.vehicleSpeed, self.speedLimitedTo,), daemon=True)
        # self._accelerateThread.start()
        # self._accelerateThread = self.executor.submit(self.speedControl.calculateAccelerationRateToLimitedSpeed,
        #                                               self.vehicleSpeed, self.speedLimitedTo)
        # self._speedMonitorThread = concurrent.futures.Future()
        # self._slowDownProgramThread = concurrent.futures.Future()
        # self._haltProgramThread = concurrent.futures.Future()

        # Start accelerating

        self._accelerateThread = threading.Thread(target=self.speedControl.calculateAccelerationRateToLimitedSpeed,
                                                  args=(self.vehicleSpeed, self.speedLimitedTo,), daemon=True)
        self._monitorSpeed = True
        self._speedMonitorThread.start()
        self._accelerateThread.start()
        self._accelerateThread.join()
        self._speedMonitorThread.join()

    def checkTrafficLightColour(self, signalColour):
        # if signalColour.name == "Green":
        #     print("\nCar sees green signal")
        # elif signalColour.name == "Red":
        #     print("\nCar sees red signal")
        # elif signalColour.name == "Yellow":
        #     print("\nCar sees yellow signal")
        self.trafficSignalColour = signalColour.name

    def setRoadLengthCovered(self, speed):
        print("\nD")

    def setTrafficSignalLocation(self, distance):
        print("\nLocation of traffic signal: ", distance)
        self.nextTrafficSignalLocationOnRoad = distance

    def speedMonitor(self):
        while self._monitorSpeed:
            time.sleep(1.0)
            self.checkDistanceToTrafficSignal()
            self.actionAccordingToTrafficSignalColourAndDistance()

    def checkDistanceToTrafficSignal(self):
        # print("current vehicle speed: ", round(self.vehicleSpeed))
        # calculate road length covered
        self.roadLengthCovered += round(self.vehicleSpeed / 3.6)
        # print("\nRoad length covered: ", self.roadLengthCovered)

        # calculate distance to signal
        self.distanceToNextSignal = self.nextTrafficSignalLocationOnRoad - self.roadLengthCovered

        # next signal
        if self.distanceToNextSignal <= 0:
            self.trafficSignalData.nextSignal()

        # print("\ndistance of signal: ", self.nextTrafficSignalLocationOnRoad)
        print("\ndistance from signal: ", self.distanceToNextSignal)

    def setSpeedLimitedTo(self, speed):
        print("\nIncrementing speed.")

    def actionAccordingToTrafficSignalColourAndDistance(self):
        # print("\nAction according called")
        # print("Deceleration lock in action: ", self.decelerationLock)
        if self.vehicleSpeed > 0:
            if 20 < self.distanceToNextSignal <= 80:
                if self.vehicleSpeed > 20:
                    self.slowDown()
                else:
                    print("\nMaintaining speed")
            elif 0 < self.distanceToNextSignal <= 20:
                if self.vehicleSpeed > 0:
                    self.stopCar()
                else:
                    print("\nVehicle stopped")
                    self._monitorSpeed = False


    def failureToReduceSpeedBefore20mtsCheck(self):
        print("\nReturn boolean")

    def setVehicleSpeed(self, speed):
        print("\nCurrent vehicle speed: ", speed)
        self.vehicleSpeed = speed
        # if not self._speedMonitorThread.running():
        #     self._speedMonitorThread = self.executor.submit(self.speedMonitor)
        # self.checkDistanceToTrafficSignal()
        # self.actionAccordingToTrafficSignalColourAndDistance()

    def slowDown(self):
        print("\nSlowing down")
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = 20
        self._slowDownProgramThread = threading.Thread(target=self.speedControl.slowDownVehicleSpeed,
                                                 args=(self.vehicleSpeed, self.speedLimitedTo,
                                                       self.distanceToNextSignal - 20,), daemon=True)
        self._slowDownProgramThread.start()
        # self._slowDownProgramThread.join()
        # self._slowDownProgramThread = self.executor.submit(self.speedControl.slowDownVehicleSpeed, self.vehicleSpeed,
        #                                                    self.speedLimitedTo,
        #                                                    self.distanceToNextSignal - 20)
        # self._slowDownProgramThread.join()

    def stopCar(self):
        print("\nStopping")
        self.speedControl.decelerating = False
        self.speedControl.accelerating = False
        self.speedControl.decelerating = True
        self.speedLimitedTo = 0
        self._haltProgramThread = threading.Thread(target=self.speedControl.bringVehicleToHalt,
                                             args=(self.vehicleSpeed, self.speedLimitedTo,
                                                   self.distanceToNextSignal,), daemon=True)
        self._haltProgramThread.start()
        # self._haltProgramThread.join()
        # self._haltProgramThread = self.executor.submit(self.speedControl.bringVehicleToHalt, self.vehicleSpeed,
        #                                                self.speedLimitedTo,
        #                                                self.distanceToNextSignal)
        # self._haltProgramThread.join()
        # print("\nHalt thread started")

    def setDecelerationLock(self, lockStatus):
        print("Deceleration lock status: ", lockStatus)
        self.decelerationLock = lockStatus
