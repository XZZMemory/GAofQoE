#程序入口
from time import clock
from Result import Result
import copy
#time_start=clock()#计时，程序开始时间
#种群初始化
import numpy
from Painter import Painter
from Population import Population
population=Population()#初始化
#population.initialization()#初始化网络拓扑
population.initializationTest()#初始化网络拓扑， 测试
#计算平均数
def getAverageNum(num):
    sum = 0
    for i in range(len(num)):
        sum += num[i]
    return sum / len(num)
def ga(population,fileName,averageFileName,typeOfVQD):
    population.initializationOfVQD(typeOfVQD)
    timeStart = clock()  # 计时，程序开始时间
    population.creatPopulation()  # 生成种群
    # 存储结果，用于绘图
    points = []
    maxFitness=0
    minFitness=0
    f = open(fileName, 'w')
    f.write(fileName+'\n')
    m=open(averageFileName,'w')
    m.write(averageFileName+'\n')
    print(str(fileName)+" VQD: "+str(population.VQD))
    '''存储结果，用于绘图，文件操作'''
    iterations = 0  # 当前迭代次数
    while (iterations < population.iterations):
        averageFitness=0
        # if(iterations%50==0):
        fitness = population.getAllFitness()  # 得到种群的适应值
        averageFitness=getAverageNum(fitness)
        if(maxFitness<averageFitness):
            maxFitness=averageFitness
        if(minFitness>averageFitness):
            minFitness=averageFitness
        #if(iterations%10==0):
        m.write("iterations "+str(iterations) + ": " + str(averageFitness) + '\n')
        f.write("iterations " + str(iterations + 1) + '\n')
        f.write(str(fitness) + '\n')
        # 将结果存入文件中
        points.append([iterations, averageFitness])
        tempPopulation = []
        while (len(tempPopulation) < population.sizeOfPopulation):
            individualForCross = population.select()# 选择--锦标赛选择法
            individualForMutate = population.crossover(individualForCross)# 交叉随机点位的交叉操作，交叉完毕之后判断是否满足约束
            ''' 交叉-返回的个体可能是空也可能交叉了，改成交叉返回的个体一定有两个，只有经过交叉的两个个体才可能变异
             变异 基本位变异，变异完毕之后判断是否满足约束条件'''
            ''' 3.变异，传入参数是两个个体，返回变异之后的两个个体，有可能是原个体，有可能是新的个体 '''
            if (len(individualForMutate) > 0):
                afterMutate = population.mutate(individualForMutate)
                for i in range(len(afterMutate)):
                    tempPopulation.append(copy.deepcopy(afterMutate[i]))
        for i in range(population.sizeOfPopulation):
            if (tempPopulation[i].getFitness() < population.individualList[i].getFitness()):
                population.individualList[i] = copy.deepcopy(tempPopulation[i])
        iterations += 1
    timeEnd = clock()
    timeDur=timeEnd-timeStart
    print("文件："+str(fileName)+"   开始时间："+str(timeStart)+"    结束时间："+str(timeEnd)+"    持续时间："+str(timeDur)+"    "+str(points))
    f.write("start time: "+str(timeStart)+'\n'+"end time: "+str(timeEnd)+'\n'+"duration time: "+str(timeEnd-timeStart))
    m.write(str(points)+'\n')
    f.close()
    m.close()
    #返回画图所需的数据
    result=Result(fileName,maxFitness,points,minFitness)
    return result

resultVQD1=ga(population,"populationOfVQD1","averagePopulationVQD1",1)
resultVQD2=ga(population,"populationOfVQD2","averagePopulationVQD2",2)
resultVQD3=ga(population,"populationOfVQD3","averagePopulationVQD3",3)
resultVQD4=ga(population,"populationOfVQD4","averagePopulationVQD4",4)
print("VQD1.points "+str(resultVQD1.points)+'\n')
print("VQD2.points "+str(resultVQD2.points)+'\n')
print("VQD3.points "+str(resultVQD3.points)+'\n')
print("VQD4.points "+str(resultVQD4.points)+'\n')
'''绘图'''

painter = Painter()
#画收敛图
print("画图")
painter.paint34(resultVQD3,resultVQD4,population.iterations)
painter.paint(resultVQD1,resultVQD2,resultVQD3,resultVQD4,population.iterations)
''' 种群迭代
'''
#利用个体0和个体1进行交叉操作，进行测试
'''
individualforCross=[]
individualforCross.append(population.individualList[0])
individualforCross.append(population.individualList[1])
after=population.crossover(individualforCross)
aftermutateindivisual=population.individualList[3].mutate()#变异执行完毕
individualforMutate=[]
individualforMutate.append(population.individualList[4])
individualforMutate.append(population.individualList[5])
aa=population.mutate(individualforMutate)#变异执行完毕
#print(clock()-time_start)#输出运行时间'''