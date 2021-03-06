import pygame, math
from collections import deque
import time

WIN_SIZE = (900, 900)
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
PATH = (0, 0, 102)
RED = ( 255, 0, 0)
GREEN = (0, 255, 0)
CELL_SIZE=20
FOUND=False


class Cell:
    def __init__(self, posx, posy, size, color, walkable, G, H, F, parent, outline, inPath):
        self.posx = posx    #both posx and posy are the coordinates
        self.posy = posy    #of a cell in pixel
        self.size = size
        self.color = color
        self.walkable=walkable
        self.G=G    #cost of a cell from the Start node
        self.H=H    #cost of a cell to the End node
        self.F=F    #simply G+H
        self.parent=parent
        self.outline=outline
        self.inPath=inPath

    def setColor(self, color): self.color = color
    def setInPath(self, inPath): self.inPath = inPath
    def setWalkable(self, walkable): self.walkable=walkable
    def setOutline(self, outline): self.outline=outline
    def getPosition(self): return [self.posx, self.posy]


def Astar(s, e, grid, screen, start_btn, font):
    found=FOUND
    open_lst=close_lst=deque()
    open_lst.append(grid[s[0]][s[1]])
    while(len(open_lst)!=0):
        open_lst=deque(sorted(open_lst, key=lambda x: x.F))
        current=open_lst.popleft()
        if current==grid[e[0]][e[1]]:
            found=True
            getPath(current, grid, screen)
            return    #path found
        else:
            if current!=grid[s[0]][s[1]]: current.setColor(RED)
            close_lst.append(current)
            currentGridPos=getGridPos(current.getPosition()[0], current.getPosition()[1])
            neighbors=getNeighbors(currentGridPos, grid)
            for neig in neighbors:
                if(neig.walkable==True):
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
        time.sleep(0.005) #manage the speed of animation
        updateGrid(screen, grid, start_btn, font)
        pygame.display.update()

    return

def getPath(e, grid, screen):
    if(e.parent[0] == -1):
        e.setColor(GREEN)
        return
    else:
        grid[e.parent[0]][e.parent[1]].setOutline(1)
        grid[e.parent[0]][e.parent[1]].setColor(PATH)
        grid[e.parent[0]][e.parent[1]].setInPath(True)
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


#get the G or the H cost, according to the euclidean method , depending on wich node, start or end node,  is given in input
def getCost(sx, sy, posx, posy):
    x=max(posx, sx)-min(posx, sx)
    y=max(posy, sy)-min(posy, sy)
    if(x==y): return x*14
    else:
        return min(x, y)*14+(max(x, y)-min(x, y))*10

#transform the pixel coordinates in maxtrix indices
def getGridPos(posx, posy):
    return (int(math.floor(posx/CELL_SIZE)), int(math.floor(posy/CELL_SIZE)))

#update color and outline of the cells before update s
def updateGrid(screen, grid, start_btn, font):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].walkable==False:grid[i][j].setOutline(0)
            if grid[i][j].inPath==True:
                grid[i][j].setColor(PATH)
                grid[i][j].setOutline(0)
            pygame.draw.rect(screen, grid[i][j].color, (grid[i][j].posx, grid[i][j].posy, grid[i][j].size, grid[i][j].size), grid[i][j].outline)
    pygame.draw.rect(screen, (255, 255, 255), start_btn, 0)
    screen.blit(font.render('Start', True, (0,0,0)), (820, 840))
    return grid

# draw start cell, end cell and wall on grid
def prepareCell(grid, screen, color, outline, walkable):
    posInGrid=getGridPos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    grid[posInGrid[0]][posInGrid[1]].walkable=walkable
    grid[posInGrid[0]][posInGrid[1]].setColor(color)
    grid[posInGrid[0]][posInGrid[1]].setOutline(outline)

    return posInGrid


def drawGrid(screen, cell_size):
    win_size=WIN_SIZE
    grid=[]
    screen.fill(WHITE)
    for i in range(0, int(win_size[0]), cell_size):
        grid_row=[]
        for j in range(0, int(win_size[0]), cell_size):
            cell=Cell(i, j, cell_size,BLACK, True, 0, 0, 0, (-1, -1), 1, False)
            grid_row.append(cell)
            pygame.draw.rect(screen, cell.color, (cell.posx, cell.posy, cell.size, cell.size), 1)
        grid.append(grid_row)
    return grid

def main():
    win_size=WIN_SIZE
    cell_size=CELL_SIZE
    found=FOUND
    white, black, blue, red, green=WHITE, BLACK, PATH, RED, GREEN
    wall_pos, start_pos, end_pos=(), (), ()
    se=1
    start_btn=pygame.Rect(800, 830 , 80, 40)
    font = pygame.font.SysFont('Arial', 25)

    screen=pygame.display.set_mode(win_size)
    pygame.display.set_caption("A* Visualization")

    grid=drawGrid(screen, cell_size)

    while not found:
        for event in pygame.event.get():

            if event.type==pygame.QUIT: return
            if event.type==pygame.KEYDOWN and event.key==pygame.K_c:
                grid=drawGrid(screen, cell_size)
                se=1
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and cell_size!=10:
            #     cell_size-=10
            #     grid=drawGrid(screen, cell_size)
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 != 700:
            #     cell_size+=10
            #     grid=drawGrid(screen, cell_size)

        # set up start cell, end cell and walls
            if(pygame.mouse.get_pressed()[2]==1 and se!=-1): #if wall
                wall_pos=prepareCell(grid, screen, black, 1, False)
            if(event.type==pygame.KEYDOWN and event.key==pygame.K_s and pygame.mouse.get_pressed()[0]==1 and se==1): #if start node
                wall_pos=prepareCell(grid, screen, green, 0, True)
                start_pos=wall_pos
                checkstart=pygame.mouse.get_pos()
                se=2
            if(event.type==pygame.KEYDOWN and event.key==pygame.K_e and pygame.mouse.get_pressed()[0]==1 and se==2): #if end node
                wall_pos=prepareCell(grid, screen, green, 0, True)
                end_pos=wall_pos
                se=0
            if(event.type==pygame.KEYDOWN and event.key==pygame.K_d and pygame.mouse.get_pressed()[0]==1):
                prepareCell(grid, screen, white, 0, True)
                updateGrid(screen, grid, start_btn, font)
                prepareCell(grid, screen, black, 1, True)
        #########################
        if (pygame.mouse.get_pos()[0] in range(800, 880) and pygame.mouse.get_pos()[1] in range(800, 870) and pygame.mouse.get_pressed()[0]==1 and se==0):
            Astar(start_pos, end_pos ,grid, screen, start_btn, font)
            se=-1

        updateGrid(screen, grid, start_btn, font)
        pygame.time.Clock().tick(120)
        pygame.display.update()

    pygame.quit()

if __name__=='__main__':
    pygame.init()
    main()
