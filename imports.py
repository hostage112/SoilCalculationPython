# -*- coding: utf-8 -*-
import csv
import codecs
import classes as data


def importNodeData():
    #Failide avamine ja haldamine
    try:
        nodesFile = codecs.open('C:\\Users\\Alex\\Dropbox\\ENDGAME\\PYTHON2\\nodes.csv', 'r', 'utf-16')
    except IOError, e:
        print "Fail ei ole leitud"
        raise e
    except Exception, e:
        print "Kuskil mujal on viga"
        raise e

    
    csv.register_dialect('ess', delimiter=';', skipinitialspace=True)
    reader = csv.reader(nodesFile, dialect='ess')
    csv.unregister_dialect('ess')
    
    nodes = {}
    
    #Eemaldan päised
    next(reader, None)
    
    for row in reader:
        name = int(row[0])
        x = float(row[1].replace(",", "."))
        y = float(row[2].replace(",", "."))
        nodes[name] = data.NodeData(name, x, y)
  
    nodesFile.close()
    
    return nodes

def importFinitElements(nodes, H):
    def calculateFinitElementCoords(corners):
        midX = 0
        midY = 0

        for node in corners:
            midX += nodes[node].x
            midY += nodes[node].y
            
        midX /= len(corners)
        midY /= len(corners)
            
        return midX, midY

    try:
        finitFile = codecs.open('C:\\Users\\Alex\\Dropbox\\ENDGAME\\PYTHON2\\finitElements.csv', 'r', 'utf-16')
    except IOError, e:
        print "Fail ei ole leitud"
        raise e
    except Exception, e:
        print "Kuskil mujal on viga"
        raise e

    csv.register_dialect('ess', delimiter=';', skipinitialspace=True)
    reader = csv.reader(finitFile, dialect='ess')
    csv.unregister_dialect('ess')

    next(reader, None)
    
    Finits = data.FinitElementData(H)
    
    for row in reader:
        name = int(row[0])
        pNorm = float(row[2].replace(",", ".")) * (-1)
        area = float(row[3].replace(",", "."))
        corners = []
        for i in range(4, len(row)):
            try:
                node = int(row[i])
                corners.append(node)
            except:
                pass
        x, y = calculateFinitElementCoords(corners)
        
        Finits.insertName(name)
        Finits.insertpNorm(pNorm)
        Finits.insertArea(area)
        Finits.insertX(x)
        Finits.insertY(y)
        Finits.insertCorners(corners)

    finitFile.close()
    
    return Finits

def importSoilData():
    try:
        soilFile = open('C:\\Users\\Alex\\Dropbox\\ENDGAME\\PYTHON2\\soil.txt', 'r')
    except IOError, e:
        print "Fail ei ole leitud"
        raise e
    except Exception, e:
        print "Kuskil mujal on viga"
        raise e

    Soil = data.SoilData()    
            
    for row in soilFile:
        splitRow = row.split(";")
        Soil.insertName(int(splitRow[0]))
        Soil.insertDepth(float(splitRow[1]))
        Soil.insertPoisson(float(splitRow[2]))

    return Soil

