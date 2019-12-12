import map_class as mp
m = mp.Map()

m.decodeMap("map.txt")
print(m.adjacency_dict)

path = m.findShortestPath("n1", 'n1')
print(path)
