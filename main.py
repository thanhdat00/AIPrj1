import Block
import Graphic
from heapq import heappush, heappop

# define position of seeker and hider
seekerRowPos = -1
seekerColPos = -1
hiderList = []

fileObject = open("Map5.txt")
input = fileObject.readline()

para = input.split(" ")
n = int(para[0])
m = int(para[1])
print(n)
print(m)

map = []

for i in range(n):
    row = []
    for j in range(m):
        row.append(-1)
    map.append(row)

rowCount = 0;
for i in range(n):
    input = fileObject.readline()
    input = input.split(" ")
    for j in range(m):
        map[i][j]  = int(input[j])
        if map[i][j] == 3:
            seekerRowPos = i
            seekerColPos = j
        if map[i][j] == 2:
            hiderList.append((i,j))

fileObject.close()
##################################################
#dfs for travers all posible cells in map

dx = [0, 1, -1, 0, -1, -1, 1, 1]
dy = [1, 0, 0, -1, -1, 1, -1, 1]
d = []
l = []
stack = []
for i in range(n):
    r  = []
    lr = []
    for j in range(m):
        r.append(-1)
        lr.append(4)
    d.append(r)
    l.append(lr)
foundPath = False
step = 0
def dfs(x,y,d,count):
    global foundPath
    if (foundPath): return
    global l
    global stack
    global step
    step += 1
    d[x][y] = count
    l[x][y] -= 1
    stack.append((x,y,step))

    pq = []

    stop = True
    for i in range(n):
        for j in range(m):
            if (map[i][j] != 1 and l[i][j] == 4):
              stop = False
              break
    foundPath = stop
    if (foundPath): return

    for i in range(8):
        nx = x + dx[i]
        ny = y + dy[i]
        if (nx >= 0  and ny >= 0 and nx < n and ny < m):
            if (d[nx][ny] == -1 and map[nx][ny] != 1):
                heappush(pq,(l[nx][ny],i))

    while (len(pq) > 0):
        (p,t) = heappop(pq)
        kx = x + dx[t]
        ky = y + dy[t]
        dfs(kx, ky, d, count + 1)
        if (foundPath): return
        step +=1
        stack.append((x,y,step))

dfs(seekerRowPos,seekerColPos,d,0)

for i in range (len(stack)):
    print(stack[i])

graphic = Graphic.Graphic(map, seekerRowPos, seekerColPos, hiderList, stack)
# point = graphic.heuristic()
# for i in range(15):
#     print(point[i])
graphic.run()
#graphic.observed()
#graphic.printBoard()
#graphic.printChecked()
