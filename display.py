from tkinter import *
import map_class as mp
import math
from PIL import Image, ImageTk


from_node_name, path, to_node_name, image, coordinates_to_name_dict, name_to_coordinates_dict, graph, coordinates, \
    img, start, finish = None, None, None, None, None, None, None, None, None, None, None
path_graphics = []
map_graphics = []
end_points_graphics = []
m = mp.Map()
counter = 0


def loadMapButton():
    main_root.focus_set()
    loadMap()
    creating_map()


def loadMap():
    global coordinates_to_name_dict, name_to_coordinates_dict, graph, coordinates
    m.clear()
    c.delete('all')
    placeUI(0)
    m.decodeMap(map_file_entry.get())
    with open(map_file_entry.get()) as f:
        f_line = f.readline()
        if f_line[0] == '#':
            filename = f_line.replace('#', '', 2).strip('\n')
            create_background_picture(filename)
    graph = m.adjacency_dict
    coordinates = m.current_vertex_coords
    coordinates_to_name_dict = m.vertex_coords_to_name
    name_to_coordinates_dict = m.vertex_name_to_coords


def creating_map():
    for Node1 in coordinates:
        x, y = int(Node1[0]), int(Node1[1])
        for Node2 in graph[coordinates_to_name_dict[Node1]]:
            x1, y1 = int(name_to_coordinates_dict[Node2[0]][0]), int(name_to_coordinates_dict[Node2[0]][1])
            map_graphics.append(c.create_line(x, y, x1, y1, width=3, fill='#1f75fe'))
    for Node in coordinates:
        x, y = int(Node[0]), int(Node[1])
        map_graphics.append(c.create_oval(x - 1, y - 1, x + 1, y + 1, width=3, fill="#1f75fe", outline="#1f75fe"))
    if img:
        c.tag_lower(img)


def creating_path(path, start, finish, line=None):
    global img, coordinates_to_name_dict, name_to_coordinates_dict, graph, path_graphics
    for el in path_graphics:
        c.delete(el)
    path_graphics = []
    for i in range(len(path[0]) - 1):
        node_name = path[0][i]
        next_node_name = path[0][i + 1]
        x_start, y_start = int(name_to_coordinates_dict[node_name][0]), int(name_to_coordinates_dict[node_name][1])
        x_finish, y_finish = int(name_to_coordinates_dict[next_node_name][0]), int(
            name_to_coordinates_dict[next_node_name][1])
        if i == len(path[0]) - 2 and i != 0:
            x4, y4 = p4((x_start, y_start), (x_finish, y_finish), (finish[0], finish[1]))
            path_graphics.append(c.create_line(finish[0], finish[1], x4, y4, width=4, fill="#6f2da8"))
            path_graphics.append(c.create_line(x4, y4, x_start, y_start, width=4, fill="#6f2da8"))
        if i == 0 and not i == len(path[0]) - 2:
            x4, y4 = p4((x_start, y_start), (x_finish, y_finish), (start[0], start[1]))
            path_graphics.append(c.create_line(start[0], start[1], x4, y4, width=4, fill="#6f2da8"))
            path_graphics.append(c.create_line(x4, y4, x_finish, y_finish, width=4, fill="#6f2da8"))
        if len(path[0]) - 2 == 0:
            x4, y4 = p4((x_start, y_start), (x_finish, y_finish), (finish[0], finish[1]))
            path_graphics.append(c.create_line(finish[0], finish[1], x4, y4, width=4, fill="#6f2da8"))
            x3, y3 = p4((x_start, y_start), (x_finish, y_finish), (start[0], start[1]))
            path_graphics.append(c.create_line(start[0], start[1], x3, y3, width=4, fill="#6f2da8"))
            path_graphics.append(c.create_line(x4, y4, x3, y3, width=3, fill="#6f2da8"))
        if not (i == len(path[0]) - 2 or i == 0 or len(path[0]) - 2 == 0):
            path_graphics.append(c.create_line(x_start, y_start, x_finish, y_finish, width=4, fill="#6f2da8"))
        for el in path_graphics:
            c.tag_raise(el)
        if not path == 'No Path!':
            travel_time_text.config(text=('Travel Time: ' + str(round(path[1], 1)) + ' minutes'))
        else:
            travel_time_text.config(text=path[1])
        for el in end_points_graphics:
            c.tag_raise(el)


def p4(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    dx, dy = x2 - x1, y2 - y1
    det = dx * dx + dy * dy
    a = (dy * (y3 - y1) + dx * (x3 - x1)) / det
    return x1 + a * dx, y1 + a * dy


def create_background_picture(file=''):
    global image, img
    pil_image = Image.open(file)
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


def e():
    global from_node_name, to_node_name, path, counter
    from_node_name, path, to_node_name = None, None, None
    c.bind("<Button 1>", closest_node_name)


def closest_node_name(event):
    global from_node_name, to_node_name, path, counter, finish, start, coordinates, end_points_graphics
    if counter == 0:
        for el in end_points_graphics:
            c.delete(el)
        end_points_graphics = []
    if not counter == 2:
        counter += 1
        x = event.x
        y = event.y
        if counter == 1:
            start = [x, y]
            end_points_graphics.append(
                c.create_oval(x - 5, y - 5, x + 5, y + 5, fill='green', outline='green'))
        else:
            finish = [x, y]
            end_points_graphics.append(
                c.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red', outline='red'))
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
        if counter == 2:
            counter = 0
            c.unbind("<Button 1>")
    if to_node_name is not None:
        path = m.findShortestPath(from_node_name, to_node_name)
        creating_path(path, start, finish)


def placeUI(offset=0):
    x = 1370 + offset
    set_route.place(x=x, y=30)
    load_map_file_button.place(x=x + 150, y=680, anchor='center')
    map_file_entry.place(x=x - 40, y=670)
    travel_time_text.place(x=x, y=80)


main_root = Tk()
main_root.geometry("{}x{}".format(1920, 1080))
main_root.title("Map of your town")
c = Canvas(main_root, height=1080, width=1200)

set_route = Button(main_root, text="New Route", width=12, height=2, command=e)
map_file_entry = Entry(main_root)
travel_time_text = Label(main_root, text='Travel Time:', font='Calibri 14')
load_map_file_button = Button(main_root, text='Load Map File', width=12, height=2, command=loadMapButton)

c.place(x=0, y=540, anchor='w')
placeUI()
main_root.mainloop()
