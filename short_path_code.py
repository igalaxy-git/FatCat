import networkx as nx

DG = nx.DiGraph()

#  граф для поля 15 на 15 где все клетки пусты
for j in range(15):
    for i in range(15 * j + 1, 15 * (j + 1)):
        eval('DG.add_edge(\'' + str(i) + '\', \'' + str(i + 1) + '\', weight=1)')

for a in range(1, 16):
    for b in range(a, a + 15 * 14, 15):
        eval('DG.add_edge(\'' + str(b) + '\', \'' + str(b + 15) + '\', weight=1)')

for j in range(15):
    for i in range(15 * j + 1, 15 * (j + 1)):
        eval('DG.add_edge(\'' + str(i + 1) + '\', \'' + str(i) + '\', weight=1)')
for a in range(1, 16):
    for b in range(a, a + 15 * 14, 15):
        eval('DG.add_edge(\'' + str(b + 15) + '\', \'' + str(b) + '\', weight=1)')
