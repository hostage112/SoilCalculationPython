import math

def Westergaard(P, dx, dy, dz, v):
    #force
    #P = Old.pNorms[j] * Old.finits[j].area
    #geometry
    #dx = abs(New.nodes[i].x - Old.finits[j].x)
    #dy = abs(New.nodes[i].y - Old.finits[j].y)
    r = (dx**2 + dy ** 2) ** (1. / 2)
    #poisson
    njuu = (1 - 2 * v) / (2 * (1 - v))
    #influence
    soilConst = 1 / (2 * math.pi)
    distInfluence = njuu ** (1./2) / ((r / dz) ** 2 + njuu) ** (3./2)
    influenceW = soilConst * distInfluence
    #pressure
    sigma = (P / (dz ** 2)) * influenceW
    return sigma
    

def Boussinesq(P, dx, dy, dz):
    #force
    #P = Old.pNorms[j] * Old.finits[j].area
    #geometry
    #dx = abs(New.nodes[i].x - Old.finits[j].x)
    #dy = abs(New.nodes[i].y - Old.finits[j].y)
    r = (dx**2 + dy ** 2) ** (1. / 2)
    #influence
    soilConst = 1 / (2 * math.pi)        
    distInfluence = 1 / ((1 + (r / dz) ** 2) ** (5. / 2))
    influenceB = 3 * soilConst * distInfluence
    #pressure
    sigma = (P / (dz ** 2)) * influenceB
    return sigma
    
v = 0.35
dz = 10.0
dx = 0.0
dy = 0.0
P = 100

R = (dx**2 + dy**2 + dz **2) ** (1. /2)

print "Bouss", Boussinesq(P, dx, dy, dz)
print "West", Westergaard(P, dx, dy, dz, v)