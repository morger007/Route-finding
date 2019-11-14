from tkinter import *
import progproj.progproj.map_class as mp


def change_mode():
    if c['background'] == "#000000":
        c['background'] = "#DCDCDC"
        c.itemconfigure('oval', outline='#000000', width=4)
    else:
        c['background'] = "#000000"
        c.itemconfigure('oval', outline='#ffffff', width=3)


all_colors = ["#ff0000", "#ff2b00",
              "#ff5500", "#ff8000",
              "#ffaa00", "#ffd500",
              "#ffff00", "#d5ff00",
              "#aaff00", "#80ff00"]
canvas_color = "#000000"
mp.Map().decodeMap("map.txt")
coordinates = mp.Map().current_vertex_coords
coordinates_to_name_dict = mp.Map().vertex_coordinates_dict
name_to_coordinates_dict = mp.Map().vertex_coordinates_dict_vol2
graph = mp.Map().adjacency_dict
path = mp.Map().findShortestPath("n0", 'n3')

# creating frame

root = Tk()
root.geometry("{}x{}".format(740, 720))
root.title("Map of your town")
c = Canvas(root, background=canvas_color, height=720, width=720)

# creating all roads

for Node1 in coordinates:
    x, y = int(Node1[0]), int(Node1[1])
    for Node2 in graph[coordinates_to_name_dict[Node1]]:
        x1, y1 = int(name_to_coordinates_dict[Node2[0]][0]), int(name_to_coordinates_dict[Node2[0]][1])
        line = c.create_line(x, y, x1, y1, width=3, fill="#1f75fe")
        c.tag_lower(line)

# creating path

for Node_name in path[0]:
    x, y = int(name_to_coordinates_dict[Node_name][0]), int(name_to_coordinates_dict[Node_name][1])
    for Node2 in graph[Node_name]:
        x1, y1 = int(name_to_coordinates_dict[Node2[0]][0]), int(name_to_coordinates_dict[Node2[0]][1])
        line = c.create_line(x, y, x1, y1, width=3, fill="#6f2da8")
        c.tag_raise(line)

# creating junctions

for Node in coordinates:
    x, y = int(Node[0]), int(Node[1])
    oval = c.create_oval(x - 1, y - 1, x + 1, y + 1, width=3, outline="#ffffff", fill="#ffffff", tag='oval')
    c.lift(oval)

# creating buttons for different modes

b1 = Button(c)
b1.place(x=700, y=680)
b1.config(relief=SUNKEN, text='D/N', width=3, height=2, command=change_mode)
c.pack(fill=BOTH)
root.configure(background='white')

root.mainloop()
