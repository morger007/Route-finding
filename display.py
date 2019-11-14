from tkinter import *
import map_class as mp


def change_mode():
    if c['background'] == "#000000":
        c['background'] = "#DCDCDC"
        c.itemconfigure('oval', outline='#000000', width=4)
        c.itemconfig(start_text, fill='black')
        c.itemconfig(destination_text, fill='black')
    else:
        c['background'] = "#000000"
        c.itemconfigure('oval', outline='#ffffff', width=3)
        c.itemconfig(start_text, fill='white')
        c.itemconfig(destination_text, fill='white')


filename = input('Sisestage kaardi failinimi: ')
mp.Map().decodeMap(filename)
print('Punktid kaardis: ' + str(mp.Map().current_vertecies))
node1 = input('Sisestage aluspunkt: ')
node2 = input('Sisestage sihtpunkt: ')


all_colors = ["#ff0000", "#ff2b00",
              "#ff5500", "#ff8000",
              "#ffaa00", "#ffd500",
              "#ffff00", "#d5ff00",
              "#aaff00", "#80ff00"]
canvas_color = "#000000"
coordinates = mp.Map().current_vertex_coords
coordinates_to_name_dict = mp.Map().vertex_name_dict
name_to_coordinates_dict = mp.Map().vertex_coordinates_dict
graph = mp.Map().adjacency_dict

path = mp.Map().findShortestPath("n3", 'n6')
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

'''
for Node_name in path[0]:
    x, y = int(name_to_coordinates_dict[Node_name][0]), int(name_to_coordinates_dict[Node_name][1])
    for Node2 in graph[Node_name]:
        x1, y1 = int(name_to_coordinates_dict[Node2[0]][0]), int(name_to_coordinates_dict[Node2[0]][1])
        line = c.create_line(x, y, x1, y1, width=3, fill="#6f2da8")
        c.tag_raise(line)
'''

for i in range(len(path[0])-1):
    node_name = path[0][i]
    next_node_name = path[0][i+1]
    x, y = int(name_to_coordinates_dict[node_name][0]), int(name_to_coordinates_dict[node_name][1])
    xF, yF = int(name_to_coordinates_dict[next_node_name][0]), int(name_to_coordinates_dict[next_node_name][1])
    line = c.create_line(x, y, xF, yF, width=3, fill="#6f2da8")
    c.tag_raise(line)

# creating junctions

for Node in coordinates:
    x, y = int(Node[0]), int(Node[1])
    oval = c.create_oval(x - 1, y - 1, x + 1, y + 1, width=3, outline="#ffffff", fill="#ffffff", tag='oval')
    c.lift(oval)

x, y = int(name_to_coordinates_dict[path[0][0]][0]), int(name_to_coordinates_dict[path[0][0]][1])
start_text = c.create_text(x-15, y-15, text='Start', font='Calibri 15', fill='white')
destination_text = c.create_text(xF-15, yF-15, text='Destination', font='Calibri 15', fill='white')

# creating buttons for different modes

b1 = Button(c)
b1.place(x=700, y=680)
b1.config(relief=SUNKEN, text='D/N', width=3, height=2, command=change_mode)
c.pack(fill=BOTH)
root.configure(background='white')

root.mainloop()
