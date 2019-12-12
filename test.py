import map_class as mp
m = mp.Map()

m.decodeMap("map.txt")
print(m.adjacency_dict)

path = m.findShortestPath("n7", 'n2')
print(path)
