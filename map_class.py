class Map:
    adjacency_dict = {}
    vertex_coords_to_name = {}
    vertex_name_to_coords = {}
    current_vertecies = []
    current_vertex_coords = []

    def clear(self):
        self.adjacency_dict = {}
        self.vertex_coords_to_name = {}
        self.vertex_name_to_coords = {}
        self.current_vertecies = []
        self.current_vertex_coords = []

    def addVertex(self, name, coords):
        current_vertecies = self.current_vertecies
        if name not in current_vertecies:
            self.vertex_coords_to_name[coords] = name
            self.vertex_name_to_coords[name] = coords
            self.current_vertex_coords.append(coords)
            self.adjacency_dict[name] = []
            current_vertecies.append(name)

    def addRoad(self, origin, destination, time, two_way):
        self.adjacency_dict[origin].append([destination, time])
        if two_way:
            self.adjacency_dict[destination].append([origin, time])

    def findShortestPath(self, origin, destination):
        path = []
        adjacency_dict = self.adjacency_dict
        visited = []
        unvisited = []
        prev_vert_and_distance_dict = {}
        current_vertecies = self.current_vertecies
        for vertex in current_vertecies:
            unvisited.append(vertex)
            prev_vert_and_distance_dict[vertex] = [vertex, 9999999999]
        prev_vert_and_distance_dict[origin] = [origin, 0]

        def dijkstra(vertex):
            current_distance = prev_vert_and_distance_dict[vertex][1]
            visited.append(vertex)
            unvisited.remove(vertex)
            for adj_vertex in adjacency_dict[vertex]:
                distance_to_adj_vert = adj_vertex[1] + current_distance
                if distance_to_adj_vert < prev_vert_and_distance_dict[adj_vertex[0]][1]:
                    prev_vert_and_distance_dict[adj_vertex[0]] = [vertex, distance_to_adj_vert]
            min_distance = 99999999
            next_vertex_to_vist = ''
            if not unvisited:
                return
            for v in unvisited:
                if prev_vert_and_distance_dict[v][1] < min_distance:
                    next_vertex_to_vist = v
                    min_distance = prev_vert_and_distance_dict[v][1]
            dijkstra(next_vertex_to_vist)

        dijkstra(origin)

        def createPath(dest):
            nonlocal path
            for vertex in prev_vert_and_distance_dict:
                if vertex == dest:
                    next_destination = prev_vert_and_distance_dict[vertex][0]
                    path.append(vertex)
                    if next_destination == dest:
                        return
                    createPath(next_destination)

        createPath(destination)
        path_lengh = prev_vert_and_distance_dict[destination][1]
        path = path[::-1]
        if len(path) == 1 and path_lengh > 0:
            return "No Path!"
        return [path, path_lengh]

    def decodeMap(self, filename):
        current_verticies = self.current_vertecies
        current_vertex_coords = self.current_vertex_coords
        addRoad = self.addRoad
        addVertex = self.addVertex
        with open(filename) as f:
            lines = f.read().split("\n")
        for line in lines:
            if not line == '' and not line[0] == '#':
                data = line.split(',')
                for i in range(len(data)):
                    data[i] = data[i].strip()
                origin = (data[1], data[2])
                dest = (data[3], data[4])
                if origin not in current_vertex_coords:
                    addVertex('n' + str(len(current_verticies)), origin)
                if dest not in current_vertex_coords:
                    addVertex('n' + str(len(current_verticies)), dest)
                if data[0] == "'two_way'":
                    two_way = True
                else:
                    two_way = False
                origin_id = current_vertex_coords.index(origin)
                dest_id = current_vertex_coords.index(dest)
                addRoad('n' + str(origin_id), 'n' + str(dest_id), float(data[5]), two_way)
