import Block
import Graphic

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
        row.append(Block.Block(-1))
    map.append(row)

# for i in range(n):
#     for j in range(m):
#         map[i][j]  =  Block()

rowCount = 0;
for i in range(n-1):
    input = fileObject.readline()
    input = input.split(" ")
    for j in range(m-1):
        map[i][j].setValue(input[j])

for i in range(n-1):
    for j in range (m-1):
        print(map[i][j].getValue())
    print("------")

       
fileObject.close()

graphic = Graphic.Graphic()
