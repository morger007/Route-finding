from tkinter import *
import map_class as mp
import math


''' connected with map creating '''


def creating_map():
    # creating all roads

    for Node1 in coordinates:
        x, y = int(Node1[0]), int(Node1[1])
        for Node2 in graph[coordinates_to_name_dict[Node1]]:
            x1, y1 = int(name_to_coordinates_dict[Node2[0]][0]), int(name_to_coordinates_dict[Node2[0]][1])
            line = c.create_line(x, y, x1, y1, width=3, fill="#1f75fe")
            c.tag_lower(line)

    # creating junctions

    creating_nodes(coordinates)


def creating_path(path, line=None):
    c.delete("all")
    creating_map()
    for i in range(len(path[0])-1):
        node_name = path[0][i]
        next_node_name = path[0][i+1]
        xStart, yStart = int(name_to_coordinates_dict[node_name][0]), int(name_to_coordinates_dict[node_name][1])
        xFinish, yFinish = int(name_to_coordinates_dict[next_node_name][0]), int(name_to_coordinates_dict[next_node_name][1])
        line = c.create_line(xStart, yStart, xFinish, yFinish, width=3, fill="#6f2da8")
        c.tag_raise(line)


def creating_nodes(coord):
    for Node in coord:
        x, y = int(Node[0]), int(Node[1])
        oval = c.create_oval(x - 1, y - 1, x + 1, y + 1, width=3, outline="#ffffff", fill="#ffffff", tag='oval')
        c.lift(oval)


''' map events '''


def edit(event):
    global from_node_name, to_node_name, path, counter
    from_node_name, path, to_node_name = None, None, None
    c.bind("<Button 1>", closest_node_name)


def change_mode():
    if c['background'] == "#000000":
        c['background'] = "#DCDCDC"
        c.itemconfigure('oval', outline='#000000', width=4)
    else:
        c['background'] = "#000000"
        c.itemconfigure('oval', outline='#ffffff', width=3)


''' path '''


def closest_node_name(event):
    global from_node_name, to_node_name, path, counter
    if counter == 2:
        counter = 0
        c.unbind("<Button 1>")
    else:
        counter += 1
        x = event.x
        y = event.y
        x_closest = None
        y_closest = None
        length = None
        for item in coordinates:
            itemx, itemy = int(item[0]), int(item[1])
            itemlen = math.sqrt((itemx - x) ** 2 + (itemy - y) ** 2)
            if length is None or itemlen < length:
                x_closest = itemx
                y_closest = itemy
                length = itemlen
        if from_node_name is None:
            from_node_name = coordinates_to_name_dict[(str(x_closest), str(y_closest))]
        else:
            to_node_name = coordinates_to_name_dict[(str(x_closest), str(y_closest))]

        print(from_node_name, to_node_name, event)
        if to_node_name is not None:
            path = mp.Map().findShortestPath(from_node_name, to_node_name)
            creating_path(path)
            creating_nodes(coordinates)


# statics & variables

counter = 0
from_node_name, path, to_node_name = None, None, None
canvas_color = "#000000"
mp.Map().decodeMap("map.txt")
coordinates = mp.Map().current_vertex_coords
coordinates_to_name_dict = mp.Map().vertex_coordinates_dict
name_to_coordinates_dict = mp.Map().vertex_coordinates_dict_vol2
graph = mp.Map().adjacency_dict

# creating frame

main_root = Tk()
main_root.geometry("{}x{}".format(740, 720))
main_root.title("Map of your town")
c = Canvas(main_root, background=canvas_color, height=720, width=720)

# day/night button

b1 = Button(c)
b1.place(x=700, y=680)
b1.config(relief=SUNKEN, text='D/N', width=4, height=2, command=change_mode)
c.pack(fill=BOTH)

# find mouse coordinates and closest node

c.bind("e", edit)
c.bind("<Button 2>", edit)

# creating map

creating_map()

main_root.mainloop()
