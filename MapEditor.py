from tkinter import *
import math
from PIL import Image, ImageTk

text = ''
road_points = []
road_graphics = []
roads = []
scale_points = []
scale_graphics = []
junct_ids = []
road_ids = [0]
state = [False, False, False, False]  # Scale, Juncts, Roads, Removing.
drawingLine, two_way = False, False
scale = 1
origin_x = 0
origin_y = 0
old_line = None
image = None
bg_image = None

line_params = ['', 'black', 2]
map_img_name = ''


def deleteElements(li, el):
    while el in li:
        ind = li.index(el)
        del li[ind]


def setState(new_state):
    global drawingLine
    stopDrawing('')
    root.focus_set()
    for i in range(4):
        state[i] = False
        if i == new_state:
            state[i] = True


def placeJunct(coords):
    if state[1]:
        button = map_canvas.create_oval(coords[0] - 5, coords[1] - 5, coords[0] + 5, coords[1] + 5,
                                        fill='black', activefill='red')
        map_canvas.tag_bind(button, '<ButtonPress-1>', lambda event, id=button, x=coords[0],
                                                              y=coords[1]: junctButton(id, x, y))


def switchWay():
    global two_way, road_type_button
    if two_way:
        road_type_button.config(bg='SystemButtonFace')
        two_way = False
    else:
        road_type_button.config(bg='green')
        two_way = True


def junctButton(id, x, y):
    global junct_ids
    global road_points, origin_x, origin_y, drawingLine, r_type
    speed = 30
    if state[3]:
        map_canvas.delete(id)
        for i in range(len(roads)):
            if not roads[i] == '':
                if (roads[i][1], roads[i][2]) == (x, y) or (roads[i][3], roads[i][4]) == (x, y):
                    for j in range(len(road_graphics[i * 2 + 1])):
                        map_canvas.delete(road_graphics[i * 2 + 1][j])
                    road_graphics[i * 2] = ''
                    road_graphics[i * 2 + 1] = ''
                    roads[i] = ''
        deleteElements(road_graphics, '')
        deleteElements(roads, '')
    if state[2]:
        try:
            speed = int(speed_entry.get())
        except ValueError:
            text_box.config(text='Please enter a number')
            pass

        pass
        if [x, y] not in road_points:
            road_points.append([x, y])
            junct_ids.append(id)
        drawingLine = True
        origin_x, origin_y = road_points[0][0], road_points[0][1]
    if len(road_points) == 2:
        x1 = road_points[0][0]
        x2 = road_points[1][0]
        y1 = road_points[0][1]
        y2 = road_points[1][1]
        length = round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 2)
        if two_way:
            roads.append(['two_way', x1, y1, x2, y2, length * 60 / speed])
        else:
            roads.append(['one_way', x1, y1, x2, y2, length * 60 / speed])
        new_road_graphics = []
        half_x = (x2 - x1) / 2
        half_y = (y2 - y1) / 2
        new_road_graphics.append(map_canvas.create_line(x2, y2, x1 + half_x, y1 + half_y, arrow='last',
                                                        arrowshape=(15, 0, 5), fill='black', width=2))
        if two_way:
            new_road_graphics.append(map_canvas.create_line(x1, y1, x1 + half_x, y1 + half_y, arrow='last',
                                                            arrowshape=(15, 0, 5), fill='black', width=2))
        main_road = map_canvas.create_line(x1, y1, x2, y2, fill='black', width=4, activefill='red')
        new_road_graphics.append(main_road)
        road_id = max(road_ids) + 1
        road_ids.append(road_id)
        map_canvas.tag_bind(main_road, '<ButtonPress-1>',
                            lambda event, id=road_id: roadButton(id))
        road_graphics.append(road_id)
        road_graphics.append(new_road_graphics)
        map_canvas.tag_raise(junct_ids[0])
        map_canvas.tag_raise(junct_ids[1])
        del road_points[0]
        del junct_ids[0]
        origin_x, origin_y = road_points[0][0], road_points[0][1]


def drawLine(event):
    global origin_x, origin_y, old_line
    if drawingLine:
        x, y = event.x, event.y
        map_canvas.delete(old_line)
        length = math.sqrt((origin_x - x) ** 2 + (origin_y - y) ** 2)
        old_line = map_canvas.create_line(origin_x, origin_y, x - (x - origin_x) * 2 / length,
                                          y - (y - origin_y) * 2 / length,
                                          width=line_params[2], fill=line_params[1], dash=line_params[0])


def stopDrawing(event):
    global drawingLine
    drawingLine = False
    map_canvas.delete(old_line)
    try:
        del road_points[0]
    except IndexError:
        pass
    try:
        del junct_ids[0]
    except IndexError:
        pass
    try:
        del scale_points[0]
    except IndexError:
        pass


def roadButton(id):
    if state[3]:
        ind = road_graphics.index(id)
        for i in range(len(road_graphics[ind + 1])):
            map_canvas.delete(road_graphics[ind + 1][i])
        del road_graphics[ind]
        del road_graphics[ind]
        del roads[int(ind / 2)]
        del road_ids[int(ind / 2)]


def save():
    with open(file_name_entry.get(), 'w') as f:
        if not map_img_name == '':
            f.write('#' + map_img_name+'#\n')
        else:
            f.write('\n')
        for road in roads:
            road[5] = round(road[5] * scale, 5)
            f.write(str(road).strip(']').strip('[') + '\n')


def defineScale(coords):
    global scale, drawingLine, origin_x, origin_y, scale_points
    if state[0]:
        scale_points.append(coords)
        for i in range(len(scale_graphics)):
            map_canvas.delete(scale_graphics[i])
            scale_graphics[i] = ''
        drawingLine = True
        line_params[0], line_params[1], line_params[2] = (50, 2), 'red', 5
        deleteElements(scale_graphics, '')
        origin_x, origin_y = scale_points[0][0], scale_points[0][1]
        if len(scale_points) == 2:
            line_params[0], line_params[1], line_params[2] = '', 'black', 2
            x1 = scale_points[0][0]
            x2 = scale_points[1][0]
            y1 = scale_points[0][1]
            y2 = scale_points[1][1]
            scale_graphics.append(map_canvas.create_line(x1, y1, x2, y2, dash=(50, 2), fill="red", width=5))
            del scale_points[0]
            del scale_points[0]
            stopDrawing('')
            try:
                r_dist = float(scale_entry.get())
                length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                scale = r_dist / length
                text_box.config(text='')
            except:
                text_box.config(text='Please enter a number')
                pass


def onClick(event):
    x = event.x
    y = event.y
    placeJunct((x, y))
    defineScale((x, y))


def loadMapImage():
    global image, map_img_name, bg_image
    filename = map_file_entry.get()
    try:
        pil_image = Image.open(filename)
        map_img_name = filename
    except:
        text_box.config(text='Please set valid map image!')
        return
    width, height = pil_image.size
    new_width = int((1080 * (width / height)))
    pil_image = pil_image.resize((new_width, 1080))
    width, height = pil_image.size
    if new_width > 1600:
        diff = new_width - 1600
        pil_image = pil_image.crop((diff, 0, width, height))
        new_width = pil_image.size[0]
    image = ImageTk.PhotoImage(pil_image)
    map_canvas.config(width=new_width)
    bg_image = map_canvas.create_image(new_width / 2, 540, image=image)
    placeUI(new_width - 1300)


def removeImage():
    global bg_image
    if bg_image:
        placeUI(0)
        map_canvas.delete(bg_image)
        bg_image = None


def placeUI(offset=0):
    x = 1370 + offset
    junct_button.place(x=x, y=70, anchor='center')
    remove_button.place(x=x, y=230, anchor='center')
    road_button.place(x=x, y=150, anchor='center')
    road_type_button.place(x=x + 100, y=150, anchor='center')
    scale_button.place(x=x, y=310, anchor='center')
    save_button.place(x=x + 150, y=680, anchor='center')
    load_map_button.place(x=x + 150, y=600, anchor='center')
    remove_image_button.place(x=x + 215, y=585)

    scale_text_box.place(x=x + 100, y=300)
    text_box.place(x=x - 50, y=350)
    file_name_entry.place(x=x - 40, y=670)
    scale_entry.place(x=x + 65, y=300)
    speed_entry.place(x=x + 150, y=140)
    speed_text_box.place(x=x + 180, y=140)
    map_file_entry.place(x=x - 40, y=590)


root = Tk()
root.geometry('1920x1080')
root.title('Map editor')
map_canvas = Canvas(root, height=1080, width=1200)
map_canvas.bind('<Button-1>', onClick)
map_canvas.place(x=0, y=540, anchor='w')

map_canvas.bind('<Motion>', drawLine)
root.bind('<Button-3>', stopDrawing)

junct_button = Button(root, text='Place Junctions', width=12, height=2, command=lambda: setState(1))
remove_button = Button(root, text='Remove', width=12, height=2, command=lambda: setState(3))
road_button = Button(root, text='Place Roads', width=12, height=2, command=lambda: setState(2))
road_type_button = Button(root, text='Two-way?', width=10, height=1, command=switchWay)
scale_button = Button(root, text='Scale', width=12, height=2, command=lambda: setState(0))
save_button = Button(root, text='save', width=12, height=2, command=save)
load_map_button = Button(root, text='Load Map Image', width=14, height=2, command=loadMapImage)
remove_image_button = Button(root, text='Remove Image', width=12, heigh=1, command=removeImage)

text_box = Label(root, text=text, font='Calibri 14', foreground='red')
scale_text_box = Label(root, text='km', font='Calibri 12')
scale_entry = Entry(root, width=3, font='Calibri 12')
speed_entry = Entry(root, width=3, font='Calibri 12')
speed_text_box = Label(root, text='km/h', font='Calibri 12')
file_name_entry = Entry(root)
map_file_entry = Entry(root)

placeUI()

mainloop()
