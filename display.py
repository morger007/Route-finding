from tkinter import Tk, Canvas, Frame, BOTH
from road_map import coordinates, graph


class PointMap(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Colours")
        self.pack(fill=BOTH, expand=1)

        c = Canvas(self)
        for key in coordinates.keys():
            print(key, coordinates[key])
            x, y = coordinates[key][0], coordinates[key][1]
            c.create_rectangle(x, y, x+1, y, width=3)
        c.pack(fill=BOTH)


def main():
    root = Tk()
    ex = PointMap(root)
    root.geometry("200x200")
    root.mainloop()


main()
