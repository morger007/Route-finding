import map_class as mp
m = mp.Map()
m.decodeMap("map.txt")
print(m.current_vertecies)
path = m.findShortestPath("n5", 'n2')
if not path == "No Path!":
    print("Found path %s of length %s" % (path[0], path[1]))
else:
    print('No Path')

