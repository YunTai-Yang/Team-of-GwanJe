class Datahub:

    def __init__ (self):
        self.rolls = []
        self.pitchs = []
        self.yaws = []
        self.rollSpeeds = []
        self.pitchSpeeds = []
        self.yawSpeeds = []
        self.Xaccels = []
        self.Yaccels = []
        self.Zaccels = []
        self.latitudes = []
        self.longitudes = []
        self.altitude = []

    def update(self,datas):

        self.rolls.append(datas[0])
        self.pitchs.append(datas[1])
        self.yaws.append(datas[2])
        self.rollSpeeds.append(datas[3])
        self.pitchSpeeds.append(datas[4])
        self.yawSpeeds.append(datas[5])
        self.Xaccels.append(datas[6])
        self.Yaccels.append(datas[7])
        self.Zaccels.append(datas[8])
        self.latitudes.append(datas[9])
        self.longitudes.append(datas[10])
        self.altitude.append(datas[11])