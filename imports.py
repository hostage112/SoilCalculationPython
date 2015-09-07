# -*- coding: utf-8 -*-
import os
import csv
import codecs
import classes as data

def importFiles(case):
    PATH, file = os.path.split(os.path.realpath(__file__))
    if (case == "test"):
        NODE = "/nodes.csv"
        FINIT = "/finitElements.csv"
        SOIL = "/soil.txt"
    elif (case == "real"):
        NODE = "/realNodes_05.csv"
        FINIT = "/realFinits_05.csv"
        SOIL = "/realSoil.txt"
        
    nodes = importNodeData(PATH + NODE)
    finits, pNorms = importFinitElements(nodes, PATH + FINIT)
    soils = importSoilData(PATH + SOIL)
        
    print "imports... done"
    return nodes, finits, pNorms, soils

def importNodeData(PATH):
    nodesFile = codecs.open(PATH, 'r', 'utf-16')
    
    csv.register_dialect('ess', delimiter=';', skipinitialspace=True)
    reader = csv.reader(nodesFile, dialect='ess')
    csv.unregister_dialect('ess')

    nodes = {}
    
    next(reader, None)
    for row in reader:
        if abs(float(row[3].replace(",", "."))) < 0.001:
            name = int(row[0])
            x = float(row[1].replace(",", "."))
            y = float(row[2].replace(",", "."))
            nodes[name] = data.NodeData(name, x, y)
  
    nodesFile.close()
    
    return nodes

def importFinitElements(nodes, PATH):
    def calculateFinitElementCoords(corners):
        midX = 0
        midY = 0

        for node in corners:
            midX += nodes[node].x
            midY += nodes[node].y
            
        midX /= len(corners)
        midY /= len(corners)
            
        return midX, midY

    finitFile = codecs.open(PATH, 'r', 'utf-16')

    csv.register_dialect('ess', delimiter=';', skipinitialspace=True)
    reader = csv.reader(finitFile, dialect='ess')
    csv.unregister_dialect('ess')

    finits = {}
    pNorms = {}

    next(reader, None)

    for row in reader:
        name = int(row[0])
        finitPnorm = float(row[2].replace(",", ".")) * (-1)
        area = float(row[3].replace(",", "."))
        corners = []
        for i in range(4, len(row)):
            try:
                node = int(row[i])
                corners.append(node)
            except:
                pass
        x, y = calculateFinitElementCoords(corners)
        
        finits[name] = data.FinitData(name, x, y, area, corners)
        pNorms[name] = finitPnorm

    finitFile.close()

    return finits, pNorms
    
def importSoilData(PATH):

    soilFile = open(PATH, 'r')

    soils = {}
            
    for row in soilFile:
        splitRow = row.split(";")
        name = int(splitRow[0])
        depth = float(splitRow[1])
        roo = float(splitRow[2])
        soils[name] = data.SoilData(name, depth, roo)

    soilFile.close()

    return soils