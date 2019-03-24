'''
需要画图，基站位置，用户位置
生成之后再画图，
'''
import matplotlib.pyplot as plt
from Result import Result
import numpy
from matplotlib.font_manager import  FontProperties

class Painter:
    def paint(self,resultVQD1,resultVQD2,resultVQD3,resultVQD4,iterations):
        maxFitness=[]
        maxFitness.append(resultVQD1.maxFitness)
        maxFitness.append(resultVQD2.maxFitness)
        maxFitness.append(resultVQD3.maxFitness)
        maxFitness.append(resultVQD4.maxFitness)
        minFitness=[]
        minFitness.append(resultVQD1.minFitness)
        minFitness.append(resultVQD2.minFitness)
        minFitness.append(resultVQD3.minFitness)
        minFitness.append(resultVQD4.minFitness)
        plt.figure(2)
        plt.title("GA", fontsize=24)
        plt.xlabel("iterations", fontsize=14)
        plt.ylabel("fitness", fontsize=14)
        plt.scatter(numpy.array(resultVQD1.points)[:, 0], numpy.array(resultVQD1.points)[:, 1], marker='.', c='black', label=resultVQD1.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例

        plt.scatter(numpy.array(resultVQD2.points)[:, 0], numpy.array(resultVQD2.points)[:, 1], marker='.', c='green',  label=resultVQD2.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.scatter(numpy.array(resultVQD3.points)[:, 0], numpy.array(resultVQD3.points)[:, 1], marker='.', c='blue', label=resultVQD3.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.scatter(numpy.array(resultVQD4.points)[:, 0], numpy.array(resultVQD4.points)[:, 1], marker='.', c='red', label=resultVQD4.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.axis([0, iterations, min(minFitness)-1,max(maxFitness)+2])
        plt.legend(
            loc='upper right')  # center left lower right right upper center lower center center right lower left best.....
        plt.show()
    #fileName,maxFitness,points)
    def paint34(self, resultVQD3, resultVQD4, iterations):
        maxFitness = []
        maxFitness.append(resultVQD3.maxFitness)
        maxFitness.append(resultVQD4.maxFitness)
        minFitness = []
        minFitness.append(resultVQD3.minFitness)
        minFitness.append(resultVQD4.minFitness)
        plt.figure(2)
        plt.title("GA", fontsize=24)
        plt.xlabel("iterations", fontsize=14)
        plt.ylabel("fitness", fontsize=14)
        plt.scatter(numpy.array(resultVQD3.points)[:, 0], numpy.array(resultVQD3.points)[:, 1], marker='.', c='blue',
                    label=resultVQD3.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.scatter(numpy.array(resultVQD4.points)[:, 0], numpy.array(resultVQD4.points)[:, 1], marker='.', c='red',
                    label=resultVQD4.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.axis([0, iterations, min(minFitness) - 1, max(maxFitness) + 1])
        plt.legend(
            loc='upper right')  # center left lower right right upper center lower center center right lower left best.....
        plt.show()
