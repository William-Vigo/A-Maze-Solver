import tkinter as tk
import math

size = 25
StartCreated = False
EndCreated = False

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.visited = False
        self.neighbors = []
        self.wall = False

class Graph:
    def __init__(self):
        self.start = tuple()
        self.end = tuple()
        self.canvas_x = 0
        self.canvas_y = 0
        self.matrix = []


    def connectGrid(self):
        x = math.ceil(self.canvas_x/size)
        y = math.ceil(self.canvas_y/size)
        self.matrix = [0]*x
        for i in range(len(self.matrix)):
            self.matrix[i] = [0]*y
        
        for i in range(x):
            for j in range(y):
                node = Node(j*size, i*size)
                self.matrix[i][j] = node
                
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                #check up
                if (i-1) >= 0:
                    self.addEdge(self.matrix[i-1][j], self.matrix[i][j])
                #check down
                if (i+1) < len(self.matrix):
                    self.addEdge(self.matrix[i+1][j], self.matrix[i][j])
                #check left
                if (j-1) >= 0:
                    self.addEdge(self.matrix[i][j-1], self.matrix[i][j])
                #check right            
                if (j+1) < len(self.matrix[i]):
                    self.addEdge(self.matrix[i][j+1], self.matrix[i][j])

    def addEdge(self, first: Node, second: Node):
        if(first not in second.neighbors):
            first.neighbors.append(second)
            second.neighbors.append(first)

        
def create_grid(g,event=None):
    canvas_x = c.winfo_width() # Get current width of canvas
    canvas_y = c.winfo_height() # Get current height of canvas
    g.canvas_x = canvas_x
    g.canvas_y = canvas_y
    g.connectGrid()
    c.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, canvas_x, size):
        c.create_line([(i, 0), (i, canvas_y)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, canvas_y, size):
        c.create_line([(0, i), (canvas_x, i)], tag='grid_line')

    
def calculateF(curr: Node, start: Node, end:Node):
    #manhatton distance
    g = abs(curr.x - start.x) + abs(curr.y - start.y)
    h = abs(end.x-curr.x) + abs(end.y - curr.y)
    return g + h

def astar(event, values):
    start = g.matrix[g.start[0]][g.start[1]]
    end = g.matrix[g.end[0]][g.end[1]]
    nodeMap = dict()
    curr = start
    nodeMap[start] = calculateF(curr, start, end)
    while(curr != end):
        curr.visited = True
        nodeMap.pop(curr)
        for neighbor in curr.neighbors:
            f_cost = calculateF(neighbor,start,end)
            if(neighbor.visited or neighbor.wall):
                continue
            if(neighbor not in nodeMap or f_cost < nodeMap[neighbor]):
                nodeMap[neighbor] = f_cost
                neighbor.parent = curr
                
        if(not nodeMap):
            print('not found')
            return
        curr = min(nodeMap, key=nodeMap.get)
        

    answer = []
    while end:
        answer.insert(0,end)
        end = end.parent
    answer.pop(0)
    answer.pop(-1)
    for i in answer:
        c.create_rectangle(i.y,i.x,i.y+size,i.x+size, fill = 'yellow')

    

def createWall(event, g):
    adjusted_x = event.x - (event.x % size)
    adjusted_y = event.y - (event.y % size)
    if not g.matrix[int(adjusted_x/size)][int(adjusted_y/size)].wall:
        #checks if position clicked is start
        if not (StartCreated and (adjusted_x == g.start[0]*size and adjusted_y == g.start[1]*size)):
            #checks if postion clicked is end
            if not (EndCreated and (adjusted_x == g.end[0]*size and adjusted_y == g.end[1]*size)):
                c.create_rectangle(adjusted_x, adjusted_y, adjusted_x + size, adjusted_y + size, fill = 'black')
                g.matrix[int(adjusted_x/size)][int(adjusted_y/size)].wall = True
def removeWall(event, g):
    adjusted_x = event.x - (event.x % size)
    adjusted_y = event.y - (event.y % size)
    if g.matrix[int(adjusted_x/size)][int(adjusted_y/size)].wall:
        c.create_rectangle(adjusted_x, adjusted_y, adjusted_x + size, adjusted_y + size, fill = 'white')
        g.matrix[int(adjusted_x/size)][int(adjusted_y/size)].wall = False
def setStart(event, g):
    global StartCreated
    if not StartCreated:
        adjusted_x = event.x - (event.x % size)
        adjusted_y = event.y - (event.y % size)
        g.start = (math.ceil(adjusted_x/size),math.ceil(adjusted_y/size))

        c.create_rectangle(adjusted_x, adjusted_y, adjusted_x + size, adjusted_y + size, fill = 'green')
        StartCreated = True

def setEnd(event, g):
    global EndCreated
    if not EndCreated:
        adjusted_x = event.x - (event.x % size)
        adjusted_y = event.y - (event.y % size)
        g.end = (math.ceil(adjusted_x/size),math.ceil(adjusted_y/size))

        c.create_rectangle(adjusted_x, adjusted_y, adjusted_x + size, adjusted_y + size, fill = 'cyan')
        EndCreated = True

root = tk.Tk()
#gets width and height of screen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()

c = tk.Canvas(root, height=h, width=w, bg='white')
c.pack(fill=tk.BOTH, expand=True)
g = Graph()
c.bind('<Configure>', lambda event, arg=g: create_grid(g, event))

c.bind('<Shift-B1-Motion>', lambda event, arg=g: createWall(event, arg))
c.bind('<Shift-Button-1>', lambda event, arg=g: setStart(event, arg))
c.bind('<Shift-Button-2>', lambda event, arg=g: setEnd(event, arg))
c.bind('<Control-B1-Motion>', lambda event, arg=g: removeWall(event, arg))
root.bind('<Return>', lambda event, arg=g: astar(event, arg))

root.mainloop()