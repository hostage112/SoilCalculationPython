class NodeData(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class FinitData(object):
    def __init__(self, x, y, area, corners):
        self.area = area
        self.corners = corners
        self.x = x
        self.y = y

P1 = NodeData(0, 0)
P2 = NodeData(2, 0)
P3 = NodeData(4, 0)
P4 = NodeData(6, 0)

P5 = NodeData(0, 2)
P6 = NodeData(2, 2)
P7 = NodeData(4, 2)
P8 = NodeData(6, 2)

P9 = NodeData(0, 4)
P10 = NodeData(2, 4)
P11 = NodeData(4, 4)
P12 = NodeData(6, 4)

P13 = NodeData(0, 6)
P14 = NodeData(2, 6)
P15 = NodeData(4, 6)
P16 = NodeData(6, 6)

Fin1 = FinitData(1, 1, 4, [P1, P2, P5, P6])
Fin2 = FinitData(3, 1, 4, [P2, P3, P6, P7])
Fin3 = FinitData(5, 1, 4, [P3, P4, P6, P8])

Fin4 = FinitData(1, 3, 4, [P5, P6, P9, P10])
Fin5 = FinitData(3, 3, 4, [P6, P7, P10, P11])
Fin6 = FinitData(5, 3, 4, [P7, P8, P11, P12])

Fin7 = FinitData(1, 5, 4, [P9, P10, P13, P14])
Fin8 = FinitData(3, 5, 4, [P10, P11, P14, P15])
Fin9 = FinitData(5, 5, 4, [P11, P12, P15, P16])