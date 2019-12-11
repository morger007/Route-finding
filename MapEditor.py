from tkinter import *
import math
text = ''
junctions = []
junct_buttons = []
road_buttons = []
road_points = []
road_graphics = []
placing_juncts = False
placing_roads = False
removing = False
two_way = False
roads = []


def remove():
    global text_box, removing, placing_juncts, placing_roads
    removing = True
    placing_juncts = False
    placing_roads = False
    text_box.config(text='Removing elements')


def placeRoad():
    global text_box, removing, placing_juncts, placing_roads
    removing = False
    placing_juncts = False
    placing_roads = True
    text_box.config(text='Placing roads')


def placingJuncts():
    global text_box, removing, placing_juncts, placing_roads
    removing = False
    placing_juncts = True
    placing_roads = False
    text_box.config(text='Placing junctions')


def placeJunct(event):
    global placing_juncts
    if placing_juncts:
        x = event.x
        y = event.y
        button = Button(root, width=5, height=7, font='none 1', command=lambda: junctButton(button))
        junct_buttons.append(Button)
        button.place(x=x, y=y)



def switchWay():
    global two_way,  road_type_button
    if two_way:
        road_type_button.config(bg='SystemButtonFace')
        two_way = False
    else:
        road_type_button.config(bg='green')
        two_way = True



def junctButton(self):
    global removing
    global road_points
    global road_graphics
    global road_buttons
    x = self.winfo_x()
    y = self.winfo_y()
    if removing:
        self.destroy()
    if placing_roads:
        if [x, y] not in road_points:
            road_points.append([x, y])
    if len(road_points) == 2:
        root.focus_set()
        x1 = road_points[0][0]
        x2 = road_points[1][0]
        y1 = road_points[0][1]
        y2 = road_points[1][1]
        length = round(math.sqrt((x1 + x2) ^ 2 + (y1 + y2) ^ 2), 2)
        if two_way:
            arrow_type = 'both'
            roads.append(['two_way', x1, y1, x2, y2, length])
        else:
            roads.append(['one_way', x1, y1, x2, y2, length])
            arrow_type = 'last'
        road_graphics.append(map_canvas.create_line(x1, y1, x2, y2, arrow=arrow_type, arrowshape=(25, 45, 10), fill="black", width=2))
        this_road_button = Button(root, width=5, height=7, font='none 1', command=lambda: roadButton(this_road_button))
        this_road_button.place(x=(x1 + x2) / 2, y=(y1 + y2) / 2)
        road_buttons.append(this_road_button)
        road_points = []


def roadButton(self):
    global removing
    if removing:
        index = road_buttons.index(self)
        map_canvas.delete(road_graphics[index])
        del road_buttons[index]
        del road_graphics[index]
        del roads[index]
        self.destroy()


def save():
    with open(file_name_entry.get(), 'w') as f:
        for road in roads:
            f.write(str(road).strip(']').strip('[') + '\n')


root = Tk()
root.geometry('1280x720')
root.title('Map editor')
map_canvas = Canvas(root, height=720, width=920, bg='green')
map_canvas.bind('<Button-1>', placeJunct)
map_canvas.place(x=0, y=360, anchor='w')
junct_button = Button(root, text='Place junctions', width=12, height=2, command=placingJuncts)
junct_button.place(x=1000, y=70, anchor='center')
remove_button = Button(root, text='Remove', width=12, height=2, command=remove)
remove_button.place(x=1000, y=230, anchor='center')
road_button = Button(root, text='Place Roads', width=12, height=2, command=placeRoad)
road_button.place(x=1000, y=150, anchor='center')
road_type_button = Button(root, text='Two-way?', width=10, height=1, command=switchWay)
road_type_button.place(x=1100, y=150, anchor='center')
save_button = Button(root, text='save', width=12, height=2, command=save)
save_button.place(x=1000, y=680, anchor='center')
text_box = Label(root, text=text, font='Calibri 14')
text_box.place(x=950, y=300)
file_name_entry = Entry(root)
file_name_entry.place(x=1060, y=670)
mainloop()
