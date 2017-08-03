import random,math
import numpy as np
from tkinter import*
from presets import*

# Rules:
# Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

TILESIZE = 2

DELAY = 0
STEP = 1


def tileMap(coords,tilesize,tag):
    canvas.delete(tag)
    [canvas.create_rectangle(pos[0]*tilesize,pos[1]*tilesize, (pos[0]*tilesize) + tilesize, (pos[1]*tilesize) + tilesize,
                             fill='black', outline='', tags=tag) for pos in coords]


def neighbor_count(pos):
    global Coordinates
    neighbors = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
    return sum(list(1 for n in neighbors if [pos[0] + n[0], pos[1] + n[1]] in Coordinates))


def simulate():
    global Coordinates,STEP
    neighbors = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    add = []
    for pos in Coordinates:
        add += list([pos[0] + n[0], pos[1] + n[1]] for n in neighbors if
                    neighbor_count([pos[0] + n[0], pos[1] + n[1]]) == 3)
    Coordinates = [pos for pos in Coordinates if neighbor_count(pos) in [2, 3]] + add
    Coordinates = [ii for n, ii in enumerate(Coordinates) if ii not in Coordinates[:n]]


def getRelativePos(event):
    canvas = event.widget
    return canvas.canvasx(event.x),canvas.canvasy(event.y)


def start():
    global Coordinates,Started,menubar
    menubar.entryconfig("Start", label="Pause", command=pause)
    menubar.entryconfig("Randomize", state='disabled')
    Started = True
    index = 0
    simulate()
    while Started and len(Coordinates) > 0:
        simulate()
        if index % STEP == 0:
            canvas.after(DELAY, simulate())
            tileMap(Coordinates, TILESIZE, 'tilemap')
        else:
            canvas.after(0, simulate())
        canvas.update()
        index += 1


def reset():
    global Coordinates,Started,menubar,TILESIZE
    menubar.entryconfig("Randomize", state='normal')
    TILESIZE = 10
    canvas.xview_moveto(float(1) / canvas.winfo_width())
    canvas.yview_moveto(float(1) / canvas.winfo_height())
    Started = False
    Coordinates = []
    tileMap(Coordinates, TILESIZE, 'tilemap')


def pause():
    global Started,menubar
    menubar.entryconfig("Randomize", state='normal')
    menubar.entryconfig("Pause", label="Start", command=start)
    Started = False


def randomize():
    global Coordinates,Started,startButton
    Started = False
    Coordinates = []
    for i in range(200):
        Coordinates.append([random.randint(0,50),random.randint(0,50)])
    tileMap(Coordinates, TILESIZE, 'tilemap')


def set_delay(delay):
    global DELAY
    DELAY = delay


def set_step(step):
    global STEP
    STEP = step


def click(event):
    x,y = getRelativePos(event)
    if [int(x/TILESIZE),int(y/TILESIZE)] not in Coordinates:
        Coordinates.append([int(x / TILESIZE), int(y / TILESIZE)])
        tileMap(Coordinates, TILESIZE, 'tilemap')
        canvas.update()


def delete(event):
    x, y = getRelativePos(event)
    for i in range(len(Coordinates)):
        if Coordinates[i] == [int(x/TILESIZE), int(y/TILESIZE)]:
            del Coordinates[i]
            break
    tileMap(Coordinates, TILESIZE, 'tilemap')
    canvas.update()


def enter_preset(name):
    global Presets,Coordinates
    if name in Presets:
        Coordinates = []
        pos = [250,250]
        for row in range(len(Presets[name])):
            for column in range(len(Presets[name][row])):
                if Presets[name][row][column] == 1:
                    Coordinates.append([int(pos[0] / TILESIZE) + column, int(pos[1] / TILESIZE) + row])
        tileMap(Coordinates, TILESIZE, 'tilemap')
        canvas.update()


def zoom(event):
    global TILESIZE,Coordinates
    if (event.delta > 0) and TILESIZE < 20:
        TILESIZE += 1
    elif (event.delta < 0) and TILESIZE > 1:
        TILESIZE -= 1
    tileMap(Coordinates, TILESIZE, 'tilemap')


def scroll_start(event):
    canvas.scan_mark(event.x, event.y)


def scroll_move(event):
    canvas.scan_dragto(event.x, event.y, gain=1)


Started = False

tk = Tk()
tk.title("John Conway's Game of Life")

menubar = Menu(tk)

presetmenu = Menu(menubar, tearoff=0)
for p in Presets:
    presetmenu.add_command(label=p, command=lambda name=p: enter_preset(name))
menubar.add_cascade(label="Presets", menu=presetmenu)

delaymenu = Menu(menubar, tearoff=0)
for d in range(0,101,20):
    delaymenu.add_command(label=str(int(d))+' ms', command=lambda delay=int(d): set_delay(delay))
menubar.add_cascade(label="Delay", menu=delaymenu)

stepmenu = Menu(menubar, tearoff=0)
stepmenu.add_command(label=str(1)+' frame', command=lambda step=1: set_step(step))
for s in range(4,21,4):
    stepmenu.add_command(label=str(int(s))+' frames', command=lambda step=int(s): set_step(step))
menubar.add_cascade(label="Step", menu=stepmenu)

menubar.add_command(label="Randomize", command=randomize)

menubar.add_command(label="Start", command=start)
menubar.add_command(label="Reset", command=reset)

tk.config(menu=menubar)


canvas = Canvas(tk,width=500,height=500)
canvas.pack()

Coordinates = []  # [[25, 25], [24, 25], [26, 25], [25, 26], [24, 26], [23, 26]]

canvas.bind("<ButtonPress-1>", scroll_start)
canvas.bind("<B1-Motion>", scroll_move)

canvas.bind('<Control-B1-Motion>',click)
canvas.bind('<B3-Motion>',delete)
canvas.bind_all('<MouseWheel>',zoom)


mainloop()
