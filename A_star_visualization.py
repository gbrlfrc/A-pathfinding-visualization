import pygame, math
from collections import deque
import time

WIN_SIZE=(700, 700)
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
BLUE = ( 0, 0, 255)
RED = ( 255, 0, 0)
GREEN = (0, 255, 0)
CELL_SIZE=20

pygame.init()
class Cell:
    def __init__(self, posx, posy, size, color, id, walkable, G, H, F, parent, outline):
        self.posx = posx
        self.posy = posy
        self.size = size
        self.color = color
        self.walkable=walkable
        self.G=G
        self.H=H
        self.F=F
        self.parent=parent
        self.outline=outline


    def setColor(self, color): self.color = color
    def setWalkable(self, walkable): self.walkable=walkable
    def ifWalkable(self): return self.walkable
    def setOutline(self): self.outline=outline
    def draw(self, screen, outline):
        pygame.draw.rect(screen, self.color, (self.posx, self.posy, self.size, self.size), outline)
    def getPosition(self): return (self.posx, self.posy)


def Astar(s, e, grid, screen):
    open_lst=close_lst=deque()
    open_lst.append(grid[s[0]][s[1]])
    while(len(open_lst)!=0):
        open_lst=deque(sorted(open_lst, key=lambda x: x.F))
        current=open_lst.popleft()

        if current==grid[e[0]][e[1]]:
            getPath(current, grid, screen)
            return    #path found
        else:
            close_lst.append(current)
            currentGridPos=getGridPos(current.getPosition()[0], current.getPosition()[1])
            neighbors=getNeighbors(currentGridPos, grid)
            for neig in neighbors:
                if(neig.ifWalkable()==True):
                    if(neig in open_lst and getCost(s[0], s[1], currentGridPos[0], currentGridPos[1])+current.G < neig.G):
                        neig.G=getCost(s[0], s[1], currentGridPos[0], currentGridPos[1])+current.G
                        neig.F=neig.G+neig.H
                        neig.parent=currentGridPos
                    elif(neig not in close_lst and neig not in open_lst):
                        neigGridPos=getGridPos(neig.getPosition()[0], neig.getPosition()[1])
                        neig.G=getCost(neigGridPos[0], neigGridPos[1], currentGridPos[0], currentGridPos[1])+current.G
                        neig.H=getCost(neigGridPos[0], neigGridPos[1], e[0], e[1])
                        neig.F=neig.G+neig.H
                        neig.parent=currentGridPos
                        open_lst.append(neig)
                        grid[neigGridPos[0]][neigGridPos[1]].setColor(GREEN)
                        grid[neigGridPos[0]][neigGridPos[1]].outline=0
    return

def getPath(e, grid, screen):
    if(e.parent[0] == -1): return
    else:
        grid[e.parent[0]][e.parent[1]].draw(screen, 0)
        e.setColor(BLUE)
        getPath(grid[e.parent[0]][e.parent[1]], grid, screen)

def getNeighbors(current_pos, grid):
    neighbors=[]
    if(current_pos[0]-1 in range(len(grid)) and current_pos[1]-1 in range(len(grid[0]))):
        neighbors.append(grid[current_pos[0]-1][current_pos[1]-1])
    if(current_pos[0]-1 in range(len(grid))):
        neighbors.append(grid[current_pos[0]-1][current_pos[1]])
    if(current_pos[0]-1 in range(len(grid)) and current_pos[1]+1 in range(len(grid[0]))):
        neighbors.append(grid[current_pos[0]-1][current_pos[1]+1])
    if(current_pos[1]-1 in range(len(grid[0]))):
        neighbors.append(grid[current_pos[0]][current_pos[1]-1])
    if(current_pos[1]+1 in range(len(grid[0]))):
        neighbors.append(grid[current_pos[0]][current_pos[1]+1])
    if(current_pos[0]+1 in range(len(grid)) and current_pos[1]-1 in range(len(grid[0]))):
        neighbors.append(grid[current_pos[0]+1][current_pos[1]-1])
    if(current_pos[0]+1 in range(len(grid))):
        neighbors.append(grid[current_pos[0]+1][current_pos[1]])
    if(current_pos[0]+1 in range(len(grid)) and current_pos[1]+1 in range(len(grid[0]))):
        neighbors.append(grid[current_pos[0]+1][current_pos[1]+1])
    return neighbors



def getCost(sx, sy, posx, posy):
    x=max(posx, sx)-min(posx, sx)
    y=max(posy, sy)-min(posy, sy)
    if(x==y): return x*14
    else:
        return min(x, y)*14+(max(x, y)-min(x, y))*10

def getGridPos(posx, posy):
    return (int(math.floor(posx/CELL_SIZE)), int(math.floor(posy/CELL_SIZE)))

def updateGrid(screen, grid, wall_pos):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if wall_pos==(i, j): grid[i][j].draw(screen, 0)
            else: grid[i][j].draw(screen, 1)
    return grid

# draw start cell, end cell and wall on grid
def prepareCell(grid, screen, color, type):
    posInGrid=getGridPos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    if(type[2]==1):
        grid[posInGrid[0]][posInGrid[1]].setWalkable(False)
        grid[posInGrid[0]][posInGrid[1]].setColor(color)
    if(type[1]==1): grid[posInGrid[0]][posInGrid[1]].setColor(color)
    if(type[0]==1): grid[posInGrid[0]][posInGrid[1]].setColor(color)
    return posInGrid


def main():
    win_size=WIN_SIZE
    cell_size=CELL_SIZE
    white, black, blue, red=WHITE, BLACK, BLUE, RED
    wall_pos, start_pos, end_pos=(), (), ()
    walls_lst=[]
    se=1

    screen=pygame.display.set_mode(win_size)
    pygame.display.set_caption("A* Visualization")
    screen.fill(white)

    id=1
    grid=[]
    for i in range(0, int(win_size[0]), cell_size):
        grid_row=[]
        for j in range(0, int(win_size[0]), cell_size):
            cell=Cell(i, j, cell_size, black, id, True, 0, 0, 0, (-1, -1), 1)
            grid_row.append(cell)
            cell.draw(screen, 1)
            id+=1
        grid.append(grid_row)


    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return

        ######################## set up start cell, end cell and walls
        if(pygame.mouse.get_pressed()[2]==1): #if wall
            wall_pos=prepareCell(grid, screen, black, (0, 0, 1))
            walls_lst.append(wall_pos)
        elif(pygame.mouse.get_pressed()[0]==1 and se==1): #if start
            wall_pos=prepareCell(grid, screen, blue, (1, 0, 0))
            start_pos=wall_pos
            checkstart=pygame.mouse.get_pos()
            se=2
        elif(pygame.mouse.get_pressed()[0]==1 and se==2 and pygame.mouse.get_pos()!=checkstart): #if end
            wall_pos=prepareCell(grid, screen, red, (0, 1, 0))
            end_pos=wall_pos
            se=0
        #########################
        if(se==0):
            Astar(start_pos, end_pos ,grid, screen)

        updateGrid(screen, grid, wall_pos)

        pygame.time.Clock().tick(60)
        pygame.display.update()


    pygame.quit()

if __name__=='__main__':
    main()
