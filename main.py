import Block
import Graphic

# define position of seeker and hider
seekerRowPos = -1
seekerColPos = -1
hiderRowPos = -1
hiderColPos = -1

fileObject = open("test1.txt")
input = fileObject.readline()

para =  input.split(" ")
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

# for i in range(n):
#     for j in range(m):
#         map[i][j]  =  Block()

rowCount = 0;
for i in range(n):
    input = fileObject.readline()
    input = input.split(" ")
    for j in range(m):
        map[i][j]  = int(input[j])
        if map[i][j] == 3:
            seekerColPos = i
            seekerColPos = j
        if map[i][j] == 2:
            hiderRowPos = i
            hiderColPos = j

for i in range(n):
    for j in range (m):
        print(map[i][j])
    print("------")

       
fileObject.close()

graphic = Graphic.Graphic(map)
graphic.run()