import map_class as mp
m = mp.Map()
m.addVertex('A', [1,2])
m.addVertex('B',[2,1])
m.addRoad('A', 'B', 2, True)
print(m.adjacency_dict)