# -*- coding: utf-8 -*-
import time
import imports
import classes as data

t1 = time.time()


Depth = -2.95
deltaDepth = 3.45

soil = imports.importSoilData()
nodes = imports.importNodeData()
H0 = imports.importFinitElements(nodes, Depth)
H0.plotSelf()
H0.findMaxPnorm()

Depth -= deltaDepth
H1 = data.FinitElementData(Depth)
H1.generateBlank(H0)
H1.generateWestgaard(H0, nodes, soil)
H1.plotSelf()
H1.findMaxPnorm()


t2 = time.time()
dt = t2 - t1
print
print "Arvutuse aeg:", dt, "s"