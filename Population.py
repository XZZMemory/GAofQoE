import random
import copy#深复制，浅复制
from Individual import Individual
class Population:
    individualList=[]#初始个体列表
    #种群各种参数设置，在这设置
    sizeOfPopulation=50#种群大小
    interations=5000#迭代次数
    crossoverPc=0.95#交叉概率
    mutatePm=1#0.02#变异概率
    '''矩阵数据均从下标0就开始存储'''
    '''1. VN矩阵，用户与视频之间的访问关系，会返回生成矩阵，在总的初始化矩阵中再调用这个函数'''
    def VNInitial(self):
        VN = []
        for i in range(0,self.sumOfVideo):
            VN.append([])
            for j in range(0,self.sumOfUE):
                n=random.uniform(0,10)
                if(n<4):
                    VN[i].append(-1)
                else:
                    VN[i].append(1)
        return VN

    ''' 2. 生成VQS矩阵，即，每个视频的描述大小,会返回生成的矩阵，在总的初始化矩阵中再调用这个函数'''
    def VQSInitial(self):
        VQS = []
        #@sum=0
        for i in range(self.sumOfVideo):
            VQS.append([])
            numofdescription = int(random.randint(9,10))
            j = 0
            while (j < numofdescription):
                sizeOfDescription = random.randint(4,5)
                VQS[i].append(sizeOfDescription)
                #sum+=sizeOfDescription
                j += 1
        #self.BScapacity=int(sum/self.numofBS)+20
        return VQS
    '''3. 基站位置的初始化。基站是4个,整个拓扑，长=宽=500m'''
    def BSLocationInitial(self):
        LocationOfBS=[[125,125],[375,125],[125,375],[375,375]]
        self.width=500
        self.height=500
        return LocationOfBS
    '''用户位置的初始化'''
    def UELocationInitial(self):
        LocationOfUE=[]
        for i in range(self.sumOfUE):
            x=random.randint(0,500)
            y=random.randint(0,500)
            LocationOfUE.append([x,y])
        return LocationOfUE
    def all_locationInitial(self):
        self.LocationOfBS=self.BSLocationInitial()#基站位置初始化
        self.LocationOfUE=self.UELocationInitial()#用户位置初始化
        self.GetVQD()#视频描述存储位置初始化
    def Initialization(self):
        self.VN=self.VNInitial()
        self.VQS=self.VQSInitial()
        self.all_locationInitial()#位置初始化
        self.BasevisitedUE=self.BaseVisitedUE()#返回函数值
        print("在初始化函数中输出每个基站的访问用户")
        print(self.BasevisitedUE)
    def __init__(self):
        self.sumofBS=4
        self.sumOfUE=9
        self.sumofchannels=10
        self.sumOfVideo=4
        self.BScapacity=[]#基站存储容量，设置每个基站的存储容量均是70，存储容量可以不一样
        for i in range(self.sumofBS):
            self.BScapacity.append(70)
        print("在初始化矩阵中输出基站容量")
        print(self.BScapacity)
    # 需要条件：用户访问视频矩阵，VQS视频的描述大小， 基站分布
    def GetVQD(self):#得到三种视频存储位置，顺序存储，随机存储，按照视频重要度，
        self.VQD1=self.GetVQD1()
        print("主函数中输出VQD1")
        for i in range(len(self.VQD1)):
            print(self.VQD1[i])
        self.VQD2=self.GetVQD2()
        print("主函数中输出VQD2")
        for i in range(len(self.VQD2)):
            print(self.VQD2[i])
        self.VQD3=self.GetVQD3()#基于视频重要度+距离确定存储位置
        print("主函数中输出VQD3")
        for i in range(len(self.VQD3)):
            print(self.VQD3[i])
    def GetVQD1(self):#顺序存储，实际是一个三维矩阵，基站+视频+描述
        VQD1=[]
        BScapacity=[]#=self.BScapacity #BScapacity=self.BScapacity#标记每个基站的声剩余存储容量
        for i in range(self.sumofBS):
            BScapacity.append(70)
        flag_of_BS=0#顺序存储，当前访问到哪个基站，初始化为0基站
        #顺序存储。，基站1-->S,用户1-->V
        for i in range(len(self.VQS)):
            VQD1.append([])
            print(flag_of_BS)
            for j in range(len(self.VQS[i])):#对于视频i的所有描述
                if (BScapacity[flag_of_BS]<self.VQS[i][j]):#当前基站不能存下这个视频
                    flag_of_BS += 1
                    if(flag_of_BS>=self.sumofBS):
                        exit("超出基站，退出")

                        '''
                    print("基站容量大，开始下一个基站")#找出问题所在，超出基站容量
                    print(flag_of_BS)
                    print(i,j)'''
                VQD1[i].append(flag_of_BS)  # 在VQD中存储当前描述存储的基站
                BScapacity[flag_of_BS] -= self.VQS[i][j]  # 当前基站的剩余容量=基站容量-视频描述大小
        return VQD1
    def GetVQD2(self):#随机存储
        BScapacity=[]#self.BScapacity#存储每个基站的容量，以得到VQD2
        for i in range(len(self.BScapacity)):
            BScapacity.append(self.BScapacity[i])
        VQD2 = []#返回的数据，视频的存储矩阵
        for i in range(len(self.VQS)):#基站
            VQD2.append([])
            for j in range(len(self.VQS[i])):#对于视频i的所第j个描述
                #随机产生一个基站（满足：基站剩余容量能够存储这个描述，否则继续产生一个随机矩阵，直至能够存储下这个描述）
                n=random.randint(0,self.sumofBS-1)#随机产生一个基站
                while(BScapacity[n]<self.VQS[i][j]):#如果基站剩余容量不能存储这个视频描述
                    n = random.randint(0, self.sumofBS - 1) #继续产生一个随机数
                VQD2[i].append(n)  # 在VQD中存储当前描述存储的基站
                BScapacity[n] -= self.VQS[i][j]  # 当前基站的剩余容量=基站容量-视频描述大小
        return VQD2
    '''3.'''
    def GetVQD3(self):#基于距离进行存储（）计算比较麻烦
        Sorted_Base_Distance=self.UEToBaseDistance(self.VN,self.LocationOfBS,self.LocationOfUE)
        BScapacity=[]
        for i in range(len(self.BScapacity)):
            BScapacity.append(self.BScapacity[i])
        #self.BScapacity#每个基站的存储容量
        print(self.BScapacity)
        print("输出基站容量")
        print(BScapacity)
        print("输出基站容量结束")
        VQD3=[]#返回的数据，视频的存储矩阵
        Video_importance=self.VideoImportanceSort(self.VN)
        print("输出视频重要度排序")
        print(Video_importance)

        for i in range(self.sumOfVideo):
            VQD3.append([])
        for i in range(len(Video_importance)):#i:0-->5,视频Video_importance[i]，0 3 1 2视频存储顺序不是按照顺序，而是按照重要度
            flag_of_Base=0
            nn=Video_importance[i]#视频nn
            for j in range(len(self.VQS[nn])):#描述大小VQS[Video_importance[i][j]#访问用户+基站位置--》视频放哪儿合适
                #找到能够存储，且距离最小的基站，1.视频的重要度 2.距离的计算（访问用户到各个基站的总距离）
                size=self.VQS[nn][j]#描述大小
                flag=0#描述>基站剩余容量
                while(flag==0):
                    if(size>BScapacity[Sorted_Base_Distance[nn][flag_of_Base]]):
                        flag_of_Base+=1
                    else:
                        flag=1
                BScapacity[Sorted_Base_Distance[nn][flag_of_Base]]-=size
                VQD3[Video_importance[i]].append(flag_of_Base)
        return VQD3
    '''3.1. 计算每个视频的每个访问用户到哪个基站的距离最近,GetVQD3函数会调用这个函数'''
    def UEToBaseDistance(self,VN,LocationOfBS,LocationOfUE):#计算每个视频的每个访问用户到哪个基站的距离最近
        MinDistance=[]
        Distance = []#计算视频访问用户到基站的距离，没有排序
        for i in range(self.sumOfVideo):#视频i 横
            Distance.append([])
            for j in range(self.sumofBS):#基站j 竖
                Distance[i].append([0,j])#加入基站标识，这样在对距离进行排序时，基站也会自动排序
                for k in range(len(VN[i])):#对于这个视频的所有访问用户k
                    if (VN[i][k] == 1):  # 用户k到基站j的距离
                        #print(LocationOfBS[j][0], LocationOfBS[j][1], LocationOfUE[k][0], LocationOfUE[k][1])
                        distance = ((LocationOfBS[j][0] - LocationOfUE[k][0])**2+(LocationOfBS[j][1] - LocationOfUE[k][1]) ** 2) ** 0.5
                        Distance[i][j][0] += distance
        #下面基于得到的距离矩阵Distance，进行排序，计算结果：视频 1-->V ,基站 距离小-->距离大
        print("输出排序后的距离（所有信息：）")
        for i in range(len(Distance)):
            print(Distance[i])
        ss=[]
        for i in range(len(Distance)):#在每一行中，即每个视频中的所有基站，基于距离进行排序（距离+基站标识），是一个三维矩阵
            nn = Distance[i]
            nn.sort(key=lambda nn: nn[0])
            ss.append(nn)
        for i in range(len(ss)):#对三维矩阵，对于每一个视频，每一行，数据原本是距离+基站标识，抽取出基站标识
            MinDistance.append([])
            for j in range(len(ss[i])):
                MinDistance[i].append(ss[i][j][1])
        print("输出排序后的基站（基于距离）")
        for i in range(len(MinDistance)):
            print(MinDistance[i])
        return MinDistance#返回基于距离排序后，基站的优先存储顺序

    '''3.2. 计算视频的访问用户数量，哪个视频比较重要（越重要，访问用户越多）,GetVQD3函数会调用这个函数'''
    def VideoImportanceSort(self,VN):#根据VN(每个视频的访问用户)，对视频的重要度排序，返回排序后的视频
        # 得到每个视频的重要程度，哪个视频访问用户多，哪个视频重要
        VideoImportance = []
        Sort_Video=[]#返回的数组
        for i in range(len(VN)):
            VideoImportance.append(0)
            for j in range(len(VN[i])):
                if (VN[i][j] == 1):  # 代表用户j访问视频i
                    VideoImportance[i] += 1
        ns=[]
        for i in range (self.sumOfVideo):
            ns.append((VideoImportance[i],i))
        #用冒泡法进行排序(×),后来找到sorted函数，[{}]
        n=sorted(ns,key=lambda ns:ns[0],reverse=True)
        for i in range(len(n)):
            Sort_Video.append(n[i][1])
        return Sort_Video
    '''4.每个基站的访问用户，在分配基站的信道和功率时会用到'''
    def BaseVisitedUE(self):
        VQD=copy.deepcopy(self.VQD2)
        #去掉列表中的重复元素
        temp_VQD=[]#视频描述的存储位置，没有 重复元素，去掉列表中的重复元素后的数组
        for i in range (len(VQD)):
            temp_VQD.append([])
            for element in VQD[i]:
                if element not in temp_VQD[i]:
                    temp_VQD[i].append(element)
        BasevisitedUE=[]#横坐标i：基站，纵坐标j：用户
        for i in range (self.sumofBS):#i：基站
            BasevisitedUE.append([])
            for j in range (len(temp_VQD)):#视频j，访问用户，没有重复元素
                for k in range(len(temp_VQD[j])):
                    if (temp_VQD[j][k]==i):#当前j视频的第k个描述存储在基站i上，找到这个视频的访问用户
                        for m in range(len(self.VN[j])):
                            if ((self.VN[j][m]!=-1)and (m not in BasevisitedUE[i])):
                                BasevisitedUE[i].append(m)
            print(BasevisitedUE[i])
            BasevisitedUE[i].sort()
        print("-------------------------------输出每个基站的访问用户-----------------")
        print(BasevisitedUE)
        return copy.deepcopy(BasevisitedUE)#返回每个基站的访问用户（根据视频描述存储位置+每个视频的访问用户）
        #基于VN（视频访问用户）和VQD
    #1.创建种群
    def creatPopulation(self):#创建种群
        for i in range(Population.sizeOfPopulation):
            print(i)
            n=Individual(self)
            print("在populatoin函数中输出创建的个体的信道分配")
            print(n.C)
            print("在populatoin函数中输出创建信道的功率分配")
            print(n.P)
            self.individualList.append(n)
    #2.交叉，返回空或者交叉之后的两个新个体，交叉操作已测试成功
    def crossover(self,individualForCross):#individualForCross是一个数组，里面有两个个体individualForCross[0],individualForCross[1]
        if (random.random()<self.crossoverPc):#小于这个概率，执行交叉操作
            print("执行交叉操作")
            individualforMutate=individualForCross[0].crossover(individualForCross[1])#individualForCross[0],individualForCross[1]均是个体individual，可以使用个体的方法
        else:#否则，不交叉
            print("不执行交叉操作")
            individualforMutate=[]
        return copy.deepcopy(individualforMutate)
    #3.变异，传入参数是两个个体，返回变异之后的两个个体，有可能是原个体，有可能是新的个体
    def mutate(self,individualForMutate):#individualForMutate存储了两个个体individualForMutate[0]和individualForMutate[1]，自己写，只有一个个体参数
        afterMutate=[]#存储经过变异处理后的个体
        for i in range(2):
            if (random.random()<self.mutatePm):#小于mutatePm，执行变异操作
                print("小于mutatePm，执行变异操作")
                afterMutate.append(individualForMutate[i].mutate())
            else:#不执行变异操作，直接将原个体加入
                print("大于mutatePm，不执行变异操作")
                afterMutate.append(individualForMutate[i])
        print("在population文件中输出变异后的两个个体")
        for i in range(len(afterMutate)):
            print(i)
            for j in range (len(afterMutate[i].C)):
                print(afterMutate[i].C[j])
            for j in range (len(afterMutate[i].P)):
                print(afterMutate[i].P[j])
        return afterMutate
    #4.得到所有个体的适应值
    def GetAllFitness(self):
        fitnessList=[]
        for i in range(self.sizeOfPopulation):
            fitnessList.append(self.individualList[i].GetFitness())#在individual文件中，这个函数的写法比较重要，好好写
        return copy.deepcopy(fitnessList)
    '''5.修改，对种群中不满足约束条件的个体进行修复，想想怎么写？？？'''
    def PopulationRevise(self):
        i=0
