from tkinter import*

GRID = [10,10]

TILESIZE = 40


def tileMap(coords,tilesize,tag):
    canvas.delete(tag)
    for x in range(GRID[0]):
        for y in range(GRID[1]):
            if [x,y] in Coordinates:
                canvas.create_rectangle(x * tilesize, y * tilesize, (x * tilesize) + tilesize,
                                        (y * tilesize) + tilesize,fill='black', outline='', tags=tag)
            else:
                canvas.create_rectangle(x * tilesize, y * tilesize, (x * tilesize) + tilesize,
                                        (y * tilesize) + tilesize, fill='', outline='light grey', tags=tag)


def click(event):
    global Coordinates
    if [int(event.x/TILESIZE),int(event.y/TILESIZE)] not in Coordinates:
        Coordinates.append([int(event.x / TILESIZE), int(event.y / TILESIZE)])
        tileMap(Coordinates, TILESIZE, 'tilemap')
        canvas.update()


def delete(event):
    for i in range(len(Coordinates)):
        if Coordinates[i] == [int(event.x/TILESIZE), int(event.y/TILESIZE)]:
            del Coordinates[i]
            break
    tileMap(Coordinates, TILESIZE, 'tilemap')
    canvas.update()


def done(event):
    global Coordinates
    rows = []
    for y in range(GRID[1]):
        rows.append([])
        for x in range(GRID[0]):
            if [x,y] in Coordinates:
                rows[-1].append(1)
            else:
                rows[-1].append(0)
    rows = [str(r)+',' for r in rows]
    print('['+'\n'.join(rows)[:-1]+']')


Coordinates = []

tk = Tk()

canvas = Canvas(tk,width=int(GRID[0]*TILESIZE),height=int(GRID[1]*TILESIZE))
canvas.pack()

tileMap(Coordinates, TILESIZE, 'tilemap')

canvas.bind('<B1-Motion>',click)
canvas.bind('<B3-Motion>',delete)
canvas.bind_all('<Return>',done)

mainloop()