class Vehicle:
    def __init__(self,type,v,posisi):
        self.type = type
        self.v = v * 1000/3600
        self.posisi = posisi


class Posisi:
    def __init__(self, x, lane):
        self.x = x
        self.lane = lane