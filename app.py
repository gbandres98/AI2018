from minesweeper import api
from minesweeper.utilities import Point, points_around_point
import random
from appJar import gui
import sys
import os
from NetworkGenerator import networkGenerator
import pgmpy.inference as pgmi  # Inferencia probabilística exacta


def start():
    app.addLabel("intro", "Welcome to fuentes' lil thing")
    app.addButtons(["Play", "Run tests (Manual)",
                    "Run tests (Fast)", "Exit"], menu)


def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)


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
        app.startSubWindow("Game lost", modal=True)
        app.addLabel("Game lost")
        app.addButton("Go back", restart)
        app.stopSubWindow()
        app.showSubWindow("Game lost")
    elif result == 2:
        print('Game won')
        draw()
        app.startSubWindow("Game won", modal=True)
        app.addLabel("Game won")
        app.addButton("Go back", restart)
        app.stopSubWindow()
        app.showSubWindow("Game won")


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


def executeRecommended():
    app.destroySubWindow("AI")
    # TODO: Execute best move (click with less probability of bomb)
    click(str(random.randint(0, 4))+','+str(random.randint(0, 4)))


def calculateAll():
    return calculate(True, True)


def calculateAndShow():
    return calculate(False, True)


def calculate(all: bool, show: bool=False):
    if (show):
        app.openSubWindow("AI")
        app.removeButton("Calculate next move")
        app.removeButton("Calculate all probabilities")
        # TODO: Add evidence, execute the bayesian network
        
        app.addLabel("I recommend <this>")
        app.addButton("Execute", executeRecommended)
        app.stopSubWindow()

def fieldState():
    cells = nonVisibleCells.copy()
    evidences = {}

    for w in range(field.width):
        for h in range(field.height):
            c = cells[w][h]
            if c.visible:
                evidences['X'+str(w)+str(h)]=0
                evidences['Y'+str(w)+str(h)]=c.value
                nonVisibleCells.remove(c)
            elif c.flagged:
                evidences['X'+str(w)+str(h)]=1
                nonVisibleCells.remove(c)

    
    return evidences

def nextMove():
    networkCopy = network.copy()
    evidences = fieldState()
    #TODO completar 'nodosDescartados' y 'casillasParaIterar'
    '''
    networkCopy.remove_nodes_from(nodosDescartados)
    networkVE = pgmi.VariableElimination(networkCopy)
    consulta = networkVE.query([casillasParaIterarSet[p]], evidences)
'''
    move = ""
    cell = [0,0]
    return [move,cell]
    

    
    

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
    location = app.getLocation()
    try:
        app.destroySubWindow("AI")
    except:
        pass
    app.startSubWindow("AI", title="Bayesian AI")
    app.setLocation(location[0]+800, location[1])
    app.addLabel("Bayesian AI")
    app.addLabel(str(field.mines_remaining()) + " Mines remaining")
    app.addButton("Calculate next move", calculateAndShow)
    app.addButton("Calculate all probabilities", calculateAll)
    app.stopSubWindow()
    app.showSubWindow("AI")


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
    w = int(app.getEntry("Width"))
    h = int(app.getEntry("Height"))
    m = int(app.getEntry("Mines"))
    global field
    global network
    global nonVisibleCells
    # DONE: Create the bayesian network for the first time
    field = api.Minefield(Point(w, h), m)
    network = networkGenerator(w,h,m)
    nonVisibleCells = field._cells
    draw()


def menu(button):
    if button == "Exit":
        app.stop()
    elif button == "Play":
        app.removeAllWidgets()
        app.addLabelNumericEntry("Width")
        app.addLabelNumericEntry("Height")
        app.addLabelNumericEntry("Mines")
        app.addButton("Go", playMenu)
    elif button == "Run tests (Manual)":
        app.stop()
    elif button == "Run tests (Fast)":
        app.stop()


app = gui('El trabajito de IA', '600x400')
app.setStartFunction(start)
app.go()
