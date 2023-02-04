from csv import writer
from time import sleep
from numpy import vstack

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
                    self.writer.writerow(data[:,i],)
                self.file.flush()
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
            sleep(0.1)
            
    def stop(self):
        if self.file != None and not self.file.closed:
            self.file.close()