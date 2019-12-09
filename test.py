import map_class as mp
m = mp.Map()

m.decodeMap("map.txt")
print(m.adjacency_dict)
print(m.current_vertecies)
print(m.current_vertex_coords)
path = m.findShortestPath("n0", 'n3')
print(path)
