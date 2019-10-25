class Map:
    adjacency_dict = {}
    vertex_coordinates_dict = {}
    current_vertecies = []

    def addVertex(self, name, coords):
        current_vertecies = self.current_vertecies
        vertex_coordinates_dict = self.vertex_coordinates_dict
        current_vertecies.append(name)
        if name not in current_vertecies:
            vertex_coordinates_dict[name] = coords
            self.adjacency_dict[name] = []

    def addRoad(self, origin, destination, time, two_way):
         self.adjacency_dict[origin] = [destination, time]
         if two_way:
             self.adjacency_dict[destination] = [origin, time]






