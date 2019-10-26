import map_class as mp
m = mp.Map()

m.addVertex('A', [0,0])
m.addVertex('B', [0,0])
m.addVertex('C', [0,0])
m.addVertex('D', [0,0])
m.addVertex('E', [0,0])
m.addRoad('A','B',5,True)
m.addRoad('A','C',6,True)
m.addRoad('B','D',3,True)
m.addRoad('C','D',2,True)
m.addRoad('D','E',1,True)
m.addRoad('C','E',4,True)

print(m.adjacency_dict)
print(m.vertex_coordinates_dict)
path = m.findShortestPath('A','E')
print(path[0],'of lengh:', path[1])