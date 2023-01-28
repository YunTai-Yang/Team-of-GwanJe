import threading
import csv
from queue import Queue
import time

class DataSaver:
    def __init__(self, datahub):

        self.datahub = datahub
        self.buffer_size = 2
        self.counter = 0
        self.file = None
        self.writer = None
        self.saverows = 0
        self.data_queue = Queue()
        self.thread = threading.Thread(target=self.saver, name='DataSaver', daemon=True)
        self.thread.start()

    def saver(self):
        while True:
            while not self.data_queue.empty():
                data = self.data_queue.get()
                self.writer.writerow(data[:])
                self.counter += 1
                if self.counter >= self.buffer_size:
                    self.counter = 0
                    self.file.flush()
            time.sleep(0.1)
                
    def save_data(self):
        while self.datahub.isdatasaver_start:
            lineRemain = len(self.datahub.timespace) - self.saverows
            if lineRemain > 0:
                for i in range(lineRemain):

                    self.data_queue.put([self.datahub.timespace[self.saverows+i][0],
                                         self.datahub.timespace[self.saverows+i][1],
                                         self.datahub.timespace[self.saverows+i][2],
                                         self.datahub.timespace[self.saverows+i][3],
                                         self.datahub.rolls[self.saverows+i],
                                         self.datahub.pitchs[self.saverows+i],
                                         self.datahub.yaws[self.saverows+i],
                                         self.datahub.rollSpeeds[self.saverows+i],
                                         self.datahub.pitchSpeeds[self.saverows+i],
                                         self.datahub.yawSpeeds[self.saverows+i],
                                         self.datahub.Xaccels[self.saverows+i],
                                         self.datahub.Yaccels[self.saverows+i],
                                         self.datahub.Zaccels[self.saverows+i],
                                         self.datahub.latitudes[self.saverows+i],
                                         self.datahub.longitudes[self.saverows+i],
                                         self.datahub.altitude[self.saverows+i]])
                    

                self.saverows += lineRemain
                
    def start(self):
        while True:

            if self.datahub.isdatasaver_start:
                if self.file is None or self.file.closed:
                    self.counter = 0
                    self.file = open(self.datahub.file_Name, 'w', newline='')

                    self.writer = csv.writer(self.file)
                    self.writer.writerow(["Hours","Minute","Second","10milis","Roll","Pitch","Yaw","RollSpeed","PitchSpeed","YawSpeed","Xaccel","Yaccel","Zaccel","longitude","latitude","altitude"])
                    self.save_data()
                    self.stop()
                else:
                    pass
            time.sleep(0.1)
            
                
    def stop(self):
        if self.file != None and not self.file.closed:
            if not self.data_queue.empty():
                while not self.data_queue.empty():
                    data = self.data_queue.get()
                    self.writer.writerow(data)
                
            self.file.close()