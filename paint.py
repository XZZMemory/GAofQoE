import numpy
import matplotlib.pyplot as plt
class paint:
    def plot_data(xx, yy):
        x=numpy.array(xx)
        y=numpy.array(yy)
        plt.figure(2)
        plt.title("GA", fontsize=24)
        plt.xlabel("iterations", fontsize=14)
        plt.ylabel("fitness", fontsize=14)
        x0, x1, x2 = x[y == 0], x[y == 1], x[y == 2]
        plt.scatter(x0[:, 0], x0[:, 1], marker='*', c='red', label=0, s=40)  # marker定义形状，label与plt.legend画出右上角图例
        plt.scatter(x1[:, 0], x1[:, 1], marker='+', c='green', label=1, s=40)  # * + o  x  s是方块 d是菱形
        plt.scatter(x2[:, 0], x2[:, 1], marker='o', c='blue', label=2, s=40)
        plt.axis([-1.5, 1.5, -1.5, 1.5])
        plt.legend(
            loc='upper right')  # center left lower right right upper center lower center center right lower left best.....
        plt.show()