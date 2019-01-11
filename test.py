import numpy

from Painter import Painter
VQS=[]
for i in range(4):
    VQS.append([])
    for j in range(2):
        VQS[i].append([])
        #是不是一个三维数组
for i in range(len(VQS)):
    for j in range(len(VQS[i])):
        for k in range(2):
            VQS[i][j].append(k)
i=2
x = numpy.array([[0, 0], [-1, 0.1], [0.3, -0.05], [0.7, 0.3], [-0.2, -0.6], [-0.15, -0.63], [-0.25, 0.55], [-0.28, 0.67]])
y = [0, 0, 0, 0, 1, 1, 2, 2]
print(max(y))