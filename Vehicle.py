class Vehicle:
    def __init__(self,type,v,posisi):
        self.type = type
        self.v = v * 1000/3600
        self.posisi = posisi
        self.adj_dist = None

    def update_speed(self,v):
        self.v = self.v + (v * 1000/3600 )

    def set_id(self,id):
        self.id = id

    def setVparams(self,vparams):
        self.vparams = vparams

    def set_adj_dist(self,dist):
        self.adj_dist = dist


    def printVehicle(self):
        print('id = ' + str(self.id),' type = ' + str(self.type) + ', v = ' + str(self.v * 3600/1000) + ' km/jam , Posisi (x) = ' + str(self.posisi.x), ', Lane = ' + str(self.posisi.lane)  + ' distance_ahead = ' + str(self.adj_dist) )

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

        v0 = None
        v1 = None
        v2 = None
        v3 = None

        if(self.v0!=None):
            v0 = self.v0 * 3600 / 1000

        if (self.v1 != None):
            v1 = self.v1 * 3600 / 1000

        if (self.v2 != None):
            v2 = self.v2 * 3600 / 1000

        if (self.v3 != None):
            v3 = self.v3 * 3600 / 1000

        print('v0 = '
              + str(v0)
        + ' ' + 'v1 = ' + str(v1)  + ' ', 'v2 = '
              + str(v2)
              + ' ', 'v3 = ' + str(v3)  + ' ')