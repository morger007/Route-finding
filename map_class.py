''''
    Todo:
    Procedural vertex naming
    ...
'''


class Map:
    adjacency_dict = {}
    vertex_coordinates_dict = {}
    current_vertecies = []

    def addVertex(self, name, coords):
        current_vertecies = self.current_vertecies
        if name not in current_vertecies:
            self.vertex_coordinates_dict[name] = coords
            self.adjacency_dict[name] = []
            current_vertecies.append(name)

    def addRoad(self, origin, destination, time, two_way):
        self.adjacency_dict[origin].append([destination, time])
        if two_way:
             self.adjacency_dict[destination] = [origin, time]


    def findShortestPath(self, origin, destination):
        path = ''
        adjacency_dict = self.adjacency_dict
        visited = []
        prev_vert_and_distance_dict = {}
        current_vertecies = self.current_vertecies
        unvisited = current_vertecies
        for vertex in current_vertecies:
            prev_vert_and_distance_dict[vertex] = ['', 99999]
        prev_vert_and_distance_dict[origin] = ['', 0]

        def dijkstra(vertex):
            if vertex not in visited:
                current_distance = prev_vert_and_distance_dict[vertex][1]
                prev_distance = 99999
                visited.append(vertex)
                next_vertex_to_visit = 'break'
                for adj_vertex in adjacency_dict[vertex]:
                    distance_to_adj_vert = adj_vertex[1] + current_distance
                    if distance_to_adj_vert < prev_vert_and_distance_dict[adj_vertex[0]][1]:
                        prev_vert_and_distance_dict[adj_vertex[0]] = [vertex, distance_to_adj_vert]
                    if adj_vertex[0] not in visited:
                        if adj_vertex[1] < prev_distance:
                            next_vertex_to_visit = adj_vertex[0]
                            prev_distance = adj_vertex[1]
                if next_vertex_to_visit == 'break':
                    return
                dijkstra(next_vertex_to_visit)

        def createPath(dest):
            nonlocal path
            for vertex in prev_vert_and_distance_dict:
                if vertex == dest:
                    next_destination = prev_vert_and_distance_dict[vertex][0]
                    path += vertex
                    if next_destination == destination:
                        return
                        break
                    createPath(next_destination)

        dijkstra(origin)
        createPath(destination)
        path_lengh = prev_vert_and_distance_dict[destination][1]
        path = path[::-1]
        return [path, path_lengh]
