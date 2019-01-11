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
#population.Initialization()#初始化网络拓扑
population.initializationTest()#初始化网络拓扑， 测试
#计算平均数
def getAverageNum(num):
    sum = 0
    for i in range(len(num)):
        sum += num[i]
    return sum / len(num)
def ga(VQD,fileName,averageFileName):
    timeStart = clock()  # 计时，程序开始时间
    population.VQD=VQD
    population.creatPopulation()  # 生成种群
    # 存储结果，用于绘图
    points = []
    maxFitness=0
    minFitness=0
    f = open(fileName, 'w')
    f.write(fileName+'\n')
    m=open(averageFileName,'w')
    m.write(averageFileName+'\n')


    '''存储结果，用于绘图，文件操作'''
    iterations = 0  # 当前迭代次数
    while (iterations < population.interations):

        # if(iterations%50==0):
        fitness = population.getAllFitness()  # 得到种群的适应值
        averageFitness=getAverageNum(fitness)
        if(maxFitness<averageFitness):
            maxFitness=averageFitness
        if(minFitness>averageFitness):
            minFitness=averageFitness
        #if(iterations%10==0):
        m.write(str(iterations) + ":" + str(averageFitness) + '\n')
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
    print(fileName)
    f.write("start:"+str(timeStart)+'\n'+"end time:"+str(timeEnd)+'\n'+"duration:"+str(timeEnd-timeStart))
    print(timeStart)
    print(timeEnd)
    print(timeEnd-timeStart)
    m.write(str(points)+'\n')

    f.close()
    m.close()
    #fileName,maxFitness,points
    result=Result(fileName,maxFitness,points,minFitness)
    return result

resultVQD1=ga(population.VQD1,"populationOfVQD1","averagePopulationVQD1")
resultVQD2=ga(population.VQD2,"populationOfVQD2","averagePopulationVQD1")
resultVQD3=ga(population.VQD3,"populationOfVQD3","averagePopulationVQD1")
'''绘图'''

painter = Painter()
#画收敛图
print("画图")
painter.paint(resultVQD1,resultVQD2,resultVQD3,population.interations)
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