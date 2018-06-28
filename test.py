from minesweeper import api
from minesweeper.utilities import Point, points_around_point
import random
from appJar import gui


def click(button):
    print(button + ' clicked')
    x = int(button.split(',')[0])
    y = int(button.split(',')[1])
    result = reveal(x, y)
    if result == 0:
        draw()
    elif result == 1:
        print('Game lost')
        draw()
    elif result == 2:
        print('Game won')
        draw()


def flag(name):
    print(name + ' flagged')
    x = int(name.split(',')[0])
    y = int(name.split(',')[1])
    cell = field[x, y]
    if not cell.visible:
        cell.flagged = not cell.flagged
    draw()


def makeFlag(label):
    def f(event): return flag(label)
    return f


def draw():
    app.removeAllWidgets()
    app.setSticky("news")
    app.setExpand("both")
    app.setFont(20)
    for x in range(0, field.width):
        for y in range(0, field.height):
            label = str(x)+','+str(y)
            app.addButton(label, click, row=x, column=y)
            app.getButtonWidget(label).bind(
                '<3>', makeFlag(label))
            app.setButton(label, str(field[x, y]))


# def game(size: Point, mines: int):
    #    playing = True
    #    while(playing):
    #        input("Continue")
    #        result = click(field, random.randint(
    #            0, size.x - 1), random.randint(0, size.y - 1))  # Random click
    #        print(repr(field))
    #        print(str(field))
    #        playing = (result == 0)
    #    if (result == 1):
    #        print('Game lost')
    #    else:
    #        print('Game won')


def reveal(x, y):
    cell = field[x, y]
    field.reveal_cell_at(Point(x, y))
    if cell.visible:
        if cell.is_mine():
            return 1
        elif field.is_fully_revealed():
            return 2
    return 0


def playMenu(button):
    w = int(app.getEntry("Weigth"))
    h = int(app.getEntry("Height"))
    m = int(app.getEntry("Mines"))
    global field
    field = api.Minefield(Point(w, h), m)
    draw()


def menu(button):
    if button == "Exit":
        app.stop()
    elif button == "Play":
        app.removeAllWidgets()
        app.addLabelNumericEntry("Weigth")
        app.addLabelNumericEntry("Height")
        app.addLabelNumericEntry("Mines")
        app.addButton("Go", playMenu)
    elif button == "Run tests (Manual)":
        app.stop()
    elif button == "Run tests (Fast)":
        app.stop()


app = gui('El trabajito de IA', '600x400')
app.addLabel("intro", "Welcome to fuentes' lil thing")
app.addButtons(["Play", "Run tests (Manual)",
                "Run tests (Fast)", "Exit"], menu)
app.go()
