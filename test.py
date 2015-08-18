import math

def Westergaard(r, v, z, P):
    njuu = (1 - 2 * v) / (2 * (1 - v))
    soilConst = (2 * math.pi)
    distInfluence = ((r / (njuu * z))** 2 + 1) ** (3. / 2)
    sigma = P / (soilConst * (njuu ** 2) * (z ** 2) * distInfluence)
    return sigma
    
    
v = 0.35
dz = 4
dx = 0.1
dy = -0.3
r = (dx**2 + dy ** 2) ** (1. / 2)
P = 100
print Westergaard(r, v, dz, P)