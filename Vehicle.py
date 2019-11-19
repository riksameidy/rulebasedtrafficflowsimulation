class Vehicle:
    def __init__(self,type,v,posisi):
        self.type = type
        self.v = v * 1000/3600
        self.posisi = posisi

    def update_speed(self,v):
        self.v = self.v + (v * 1000/3600 )

    def set_id(self,id):
        self.id = id

    def setVparams(self,vparams):
        self.vparams = vparams

    def printVehicle(self):
        print('type = ' + str(self.type) + ', v = ' + str(self.v * 3600/1000) + ' km/jam , Posisi (x) = ' + str(self.posisi.x), ', Lane = ' + str(self.posisi.lane) )

class Posisi:
    def __init__(self, x, lane):
        self.x = x
        self.lane = lane

class ParamState:
    def __init__(self,C,discount):
        self.C = C
        self.discount = discount

class Vparams:
    def __init__(self,v0,v1,v2,v3):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    def printVparams(self):
        print('v0 = ' + str(self.v0)  + ' ' + 'v1 = ' + str(self.v1)  + ' ', 'v2 = ' + str(self.v2)  + ' ', 'v3 = ' + str(self.v3)  + ' ')