from tkinter import *
import map_class as mp
import math


def change_mode():
    if c['background'] == "#000000":
        c['background'] = "#DCDCDC"
        c.itemconfigure('oval', outline='#000000', width=4)
    else:
        c['background'] = "#000000"
        c.itemconfigure('oval', outline='#ffffff', width=3)


def fi(event):
    b2 = Button(c, text="To", height=1, width=5)
    b3 = Button(c, text="From", height=1, width=5)
    b3.place(x=0, y=2)
    b2.place(x=0, y=20)

    c.bind("<Button 1>", closest_node_name)


def creating_path(path):
    for i in range(len(path[0])-1):
        node_name = path[0][i]
        next_node_name = path[0][i+1]
        x, y = int(name_to_coordinates_dict[node_name][0]), int(name_to_coordinates_dict[node_name][1])
        xF, yF = int(name_to_coordinates_dict[next_node_name][0]), int(name_to_coordinates_dict[next_node_name][1])
        line = c.create_line(x, y, xF, yF, width=3, fill="#6f2da8")
        c.tag_raise(line)


def closest_node_name(event):
    global from_node_name, to_node_name
    x = event.x
    y = event.y
    x_closest = None
    y_closest = None
    lenght = None
    for item in coordinates:
        itemx, itemy = int(item[0]), int(item[1])
        itemlen = math.sqrt((itemx - x) ** 2 + (itemy - y) ** 2)
        if lenght is None or itemlen < lenght:
            x_closest = itemx
            y_closest = itemy
            lenght = itemlen
    if from_node_name is None:
        from_node_name = coordinates_to_name_dict[(str(x_closest), str(y_closest))]
        c.bind("<Button 1>", closest_node_name)
    else:
        to_node_name = coordinates_to_name_dict[(str(x_closest), str(y_closest))]
    print(to_node_name, from_node_name, event)
    if to_node_name is not None:
        path = mp.Map().findShortestPath(from_node_name, to_node_name)
        creating_path(path)


from_node_name = None
to_node_name = None
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

# creating all roads

for Node1 in coordinates:
    x, y = int(Node1[0]), int(Node1[1])
    for Node2 in graph[coordinates_to_name_dict[Node1]]:
        x1, y1 = int(name_to_coordinates_dict[Node2[0]][0]), int(name_to_coordinates_dict[Node2[0]][1])
        line = c.create_line(x, y, x1, y1, width=3, fill="#1f75fe")
        c.tag_lower(line)


# find mouse coordinates and closest node
c.bind("<Button 2>", fi)
print(coordinates)


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
main_root.configure(background='white')

main_root.mainloop()
