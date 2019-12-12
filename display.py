from tkinter import *
import map_class as mp

import math
from PIL import Image, ImageTk

''' connected with map creating '''

from_node_name, path, to_node_name, image, coordinates_to_name_dict, name_to_coordinates_dict, graph, coordinates, img = None, None, None, None, None, None, None, None, None
arrows = []

def loadMapButton():
    loadMap()
    creating_map()

def loadMap():
    global coordinates_to_name_dict, name_to_coordinates_dict, graph, coordinates
    mp.Map().decodeMap("map.txt")
    coordinates = mp.Map().current_vertex_coords
    coordinates_to_name_dict = mp.Map().vertex_coords_to_name
    name_to_coordinates_dict = mp.Map().vertex_name_to_coords
    graph = mp.Map().adjacency_dict
    print(graph)

def creating_map():
    # creating all roads
    for Node1 in coordinates:
        x, y = int(Node1[0]), int(Node1[1])
        for Node2 in graph[coordinates_to_name_dict[Node1]]:
            x1, y1 = int(name_to_coordinates_dict[Node2[0]][0]), int(name_to_coordinates_dict[Node2[0]][1])
            line = c.create_line(x, y, x1, y1, width=3, fill="#1f75fe")
            c.tag_lower(line)
        Label(main_root, text=coordinates_to_name_dict[(Node1[0], Node1[1])]).place(x=x, y=y)
    # creating junctions

    creating_nodes(coordinates)


def creating_path(path, line=None):
    global img, coordinates_to_name_dict, name_to_coordinates_dict, graph, arrows
    arrows = []
    c.delete("all")
    creating_map()
    if img:
        create_background_picture()
        c.tag_lower(img)
    for i in range(len(path[0]) - 1):
        node_name = path[0][i]
        next_node_name = path[0][i + 1]

        xStart, yStart = int(name_to_coordinates_dict[node_name][0]), int(name_to_coordinates_dict[node_name][1])
        xFinish, yFinish = int(name_to_coordinates_dict[next_node_name][0]), int(
        name_to_coordinates_dict[next_node_name][1])
        line = c.create_line(xStart, yStart, xFinish, yFinish, width=3, fill="#6f2da8")
        c.tag_raise(line)
        print(path)
        if not path == 'No Path!':
            travel_time_text.config(text=('Travel Time: ' + str(path[1])))
        else:
            travel_time_text.config(text=path[1])


def creating_nodes(coord):
    for Node in coord:
        x, y = int(Node[0]), int(Node[1])
        oval = c.create_oval(x - 1, y - 1, x + 1, y + 1, width=3, outline="#1f75fe", fill="#1f75fe", tag='oval')
        c.lift(oval)


def create_background_picture():
    global image, img
    filename = map_img_entry.get()
    pil_image = Image.open(filename)
    width, height = pil_image.size
    new_width = int((1080 * (width / height)))
    pil_image = pil_image.resize((new_width, 1080))
    width, height = pil_image.size
    if new_width > 1600:
        diff = new_width - 1600
        pil_image = pil_image.crop((diff, 0, width, height))
        new_width = pil_image.size[0]
    image = ImageTk.PhotoImage(pil_image)
    img = c.config(width=new_width)
    img = c.create_image(new_width / 2, 540, image=image)
    placeUI(new_width - 1300)
    c.tag_lower(img)


''' map events '''


def e():
    global from_node_name, to_node_name, path, counter
    from_node_name, path, to_node_name = None, None, None
    c.bind("<Button 1>", closest_node_name)


''' path '''


def closest_node_name(event):
    global from_node_name, to_node_name, path, counter, coordinates
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
    print(path)


def placeUI(offset=0):
    x = 1370 + offset
    load_map_button.place(x=x + 150, y=600, anchor='center')
    map_img_entry.place(x=x - 40, y=590)
    set_route.place(x=x, y=30)
    load_map_file_button.place(x=x + 150, y=680, anchor='center')
    map_file_entry.place(x=x - 40, y=670)
    travel_time_text.place(x=x, y=80)


# statics & variables


counter = 0

# creating frame


main_root = Tk()
main_root.geometry("{}x{}".format(1920, 1080))
main_root.title("Map of your town")
c = Canvas(main_root, height=1080, width=1200)

# edit


set_route = Button(main_root, text="New Route", width=12, height=2, command=e)
map_img_entry = Entry(main_root)
map_file_entry = Entry(main_root)
travel_time_text = Label(main_root, text='Travel Time:', font='Calibri 14')
load_map_file_button = Button(main_root, text='Load Map File', width=12, height=2, command=loadMapButton)
load_map_button = Button(main_root, text='Load Map Image', width=12, height=2, command=create_background_picture)
c.place(x=0, y=540, anchor='w')

# creating map
placeUI()

main_root.mainloop()
