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
        self.adjacency_dict[origin] = [destination, time]
        if two_way:
            self.adjacency_dict[destination] = [origin, time]
