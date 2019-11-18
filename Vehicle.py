class Vehicle:
    def __init__(self,type,v,posisi):
        self.type = type
        self.v = v * 1000/3600
        self.posisi = posisi

    def printVehicle(self):
        print('type = ' + str(self.type) + ', v = ' + str(self.v * 3600/1000) + ' km/jam , Posisi (x) = ' + str(self.posisi.x), ', Lane = ' + str(self.posisi.lane) )

class Posisi:
    def __init__(self, x, lane):
        self.x = x
        self.lane = lane

