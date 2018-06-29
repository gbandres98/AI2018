import pgmpy.models as pgmm  # Modelos gráficos de probabilidad
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales y
                                       # factores de probabilidad
from itertools import product

def networkGenerator(width,height,mines):
    
    nodesX = []
    nodesY = []
    edges = []
    cpdsY = []
    # http://thomas-cokelaer.info/blog/2012/11/how-do-use-itertools-in-python-to-build-permutation-or-combination/
    posibilities3 = list(product([0,1], repeat=3))
    posibilities5 = list(product([0,1], repeat=5))
    posibilities8 = list(product([0,1], repeat=8))

    for w in range(width):
        for h in range(height):
            neighbours = []

            x = 'X'+str(w)+str(h)
            y = 'Y'+str(w)+str(h)
            nodesX.append(x)
            nodesY.append(y)
            
            y1 = 'Y'+str(w+1)+str(h)
            y2 = 'Y'+str(w+1)+str(h+1)
            y3 = 'Y'+str(w)+str(h+1)
            y4 = 'Y'+str(w-1)+str(h+1)
            y5 = 'Y'+str(w-1)+str(h)
            y6 = 'Y'+str(w-1)+str(h-1)
            y7 = 'Y'+str(w)+str(h-1)
            y8 = 'Y'+str(w+1)+str(h-1)
            
            #Top left cell
            if(w==0 and h==0):
                neighbours = [y1,y2,y3]
            #Bottom left cell
            elif(w==0 and h==height-1):
                neighbours = [y1,y7,y8]
            #top right cell
            elif( w==width-1 and h==0):
                neighbours = [y3,y4,y5]
            #bottom right cell
            elif(w==width-1 and h==height-1):
                neighbours = [y5,y6,y7]
            #left side cells
            elif(w==0):
                neighbours = [y1,y2,y3,y7,y8]
            #right side cells
            elif(w==width-1):
                neighbours = [y3,y4,y5,y6,y7]
            #top cells
            elif(h==0):
                neighbours = [y1,y2,y3,y4,y5]
            #bottom cells
            elif(h==height-1):
                neighbours = [y1,y5,y6,y7,y8]       
            #middle cells
            else:
                neighbours = [y1,y2,y3,y4,y5,y6,y7,y8]

            for n in neighbours:
                edges.append((x,n))
            length = len(neighbours)
            p = []
            posibilities = []
            if(length==8):
                posibilities = posibilities8.copy()
            elif length==5:
                posibilities = posibilities5.copy()
            else:
                posibilities = posibilities3.copy()
            
            #Calculate Y cpds
            valuesTotal = []
            for v in range(length+1):
                values = []
                for p in posibilities:
                    n=0
                    for b in p: 
                        n = n + b
                    if n == v:
                        values.append(1)
                    else:
                        values.append(0)
                valuesTotal.append(values)

            #the Y cardinality is 1 for each X as a mine and one more if all X=0
            #evidence for Y are the surrounding Xs
            #evidence cardinality, X can only take 2 valuesTotal
            ev_card = [2]*length
            cpd = pgmf.TabularCPD(y,length+1,valuesTotal,neighbours,ev_card)
            cpdsY.append(cpd)
    
    
    #Create model
    Model_minesweeper = pgmm.BayesianModel()
    
    #Add all nodes
    Model_minesweeper.add_nodes_from(nodesX)
    Model_minesweeper.add_nodes_from(nodesY)

    #Add all edgesAux
    Model_minesweeper.add_edges_from(edges)

    #Add all cpds
    minesPerCell = mines/(width*height)
    for e in nodesX:
        cpd = pgmf.TabularCPD(e,2,[[1 - minesPerCell,minesPerCell]])
        Model_minesweeper.add_cpds(cpd)
    for e in cpdsY:
        Model_minesweeper.add_cpds(e)
    
    return Model_minesweeper
    #for m in Model_minesweeper.cpds: print(m)
  #  neighbours = []
  #  neighbours.append([('X00','Y01'),('X00','Y10')])
  #  print(neighbours)
  #  Model_minesweeper.add_edges_from(neighbours)
  #  print(Model_minesweeper.edgesAux())