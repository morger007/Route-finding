from tkinter import Tk, Canvas, Frame, BOTH
from road_map import coordinates, graph, boolean_graph


class PointMap(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Map of your town")
        self.pack(fill=BOTH, expand=1)
        all_colors = ["#ff0000", "#ff2b00",
                      "#ff5500", "#ff8000",
                      "#ffaa00", "#ffd500",
                      "#ffff00", "#d5ff00",
                      "#aaff00", "#80ff00"]
        c = Canvas(self, bg="#000000")
        for Node1 in coordinates.keys():
            x, y = coordinates[Node1][1], coordinates[Node1][2]
            for Node2 in graph[Node1]:
                x1, y1 = coordinates[Node2][1], coordinates[Node2][2]
                color_number = boolean_graph[coordinates[Node1][0]][coordinates[Node2][0]]

                c.create_line(x, y, x1, y1, width=3, fill=all_colors[color_number])
            c.create_rectangle(x, y, x + 1, y, width=3, outline="#ffffff")

        c.pack(fill=BOTH)


def main():
    root = Tk()
    ex = PointMap(root)
    root.geometry("200x200")
    root.mainloop()


main()
