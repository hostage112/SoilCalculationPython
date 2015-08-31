import math

def Westergaard(r, v, z, P):
    njuu = (1 - 2 * v) / (2 * (1 - v))
    soilConst = (2 * math.pi)
    distInfluence = ((r / (njuu * z))** 2 + 1) ** (3. / 2)
    sigma = P / (soilConst * (njuu) * (z ** 2) * distInfluence)
    return sigma
    

def Boussinesq(R, z, P):
    soilConst = (2 * math.pi)        
    distInfluence = (z ** 3) / (R ** 5)
    sigma = (3 * P) * distInfluence / soilConst 
    return sigma
    
v = 0.35
dz = 1.0
dx = 1.0
dy = 1.0
r = (dx**2 + dy ** 2) ** (1. / 2)
P = 100

R = (dx**2 + dy**2 + dz **2) ** (1. /2)

print Westergaard(r, v, dz, P)
print Boussinesq(R, dz, P)