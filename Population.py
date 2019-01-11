import random
import copy#深复制，浅复制
from Individual import Individual
class Population:
    #类似于类变量，各个函数都可以使用
    individualList=[]#初始个体列表
    #种群参数设置
    sizeOfPopulation=50#测试，先写10个种群大小
    interations=3000#迭代次数
    crossoverPc=0.95#交叉概率
    mutatePm=0.02#0.02#变异概率
    '''
    1.初始化 1-VN
             2-VQS
             3-location(BS、UE)，VQD
             4-BasevisitedUE
             5-BScapacity
    2.creatPopulation
    3.crossover
    4.mutate
    5.GetAllFitness，**
    6.PopulationRevise？？   后续适应值低会自动淘汰掉'''
    def initialization(self):
        #self.VN=self.VNInitial()
        self.VN=[[-1, -1, 1, 1, -1, 1, -1, -1, 1], [-1, 1, -1, 1, 1, -1, 1, -1, -1], [-1, 1, -1, 1, 1, 1, -1, 1, -1], [-1, 1, 1, -1, -1, -1, -1, 1, -1]]
        #self.VQS=self.VQSInitial()
        self.VQS=[[5, 4, 5, 4, 5, 4, 4, 4, 5], [5, 5, 5, 4, 4, 5, 4, 5, 4], [5, 5, 5, 5, 5, 5, 5, 5, 4], [4, 4, 5, 5, 4, 4, 4, 4, 5]]
        self.allLocationInitial()#位置初始化
        self.baseVisitedUE=self.getBaseVisitedUE()#返回函数值
    #测试
    def initializationTest(self):
        self.VN=[[1, -1, 1, -1, -1, -1, 1, 1, -1], [-1, 1, 1, -1, 1, -1, 1, 1, 1], [-1, -1, -1, -1, -1, -1, 1, 1, -1], [-1, -1, 1, 1, -1, -1, -1, 1, 1]]
        self.VQS=[[4, 5, 4, 5, 4, 5, 4, 5, 5], [4, 5, 4, 4, 5, 5, 4, 5, 5], [4, 4, 5, 5, 4, 4, 5, 5, 4], [4, 4, 5, 4, 4, 5, 4, 5, 5]]
        self.locationOfBase =[[0,0], [0,100], [100,0], [100,100]] # 基站位置初始化
        self.locationOfUser =[[25,0], [50,0], [75,0], [0,25], [0,50], [0,75], [25,25], [25,50], [50,50]] # 用户位置初始化
        self.getVQD()  # 视频描述存储位置初始化
        self.VQD1 =[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1],     [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 2, 2, 2, 2, 2, 2, 2]]  # 顺序存储
        self.VQD2 =[[1, 1, 1, 1, 1, 1, 2, 2, 0], [1, 3, 2, 3, 3, 1, 1, 3, 3], [3, 1, 1, 3, 1, 1, 2, 2, 0], [1, 3, 0, 2, 2, 1, 2, 2, 3]]  # 随机存储
        self.VQD3 =[[0, 0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0]]  # 基于视频重要度+距离确定存储位置
        self.basevisitedUE = self.getBaseVisitedUE()  # 返回函数值，每个基站的访问用户，在基站分配信道时使用
    def __init__(self):
        self.sumOfBase=4
        self.sumOfUser=9
        self.sumOfChannels=10
        self.sumOfVideo=4
        self.baseCapacity=[]#基站存储容量，设置每个基站的存储容量均是70，存储容量可以不一样
        for i in range(self.sumOfBase):
            self.baseCapacity.append(70)
        self.VQD=[]
    def allLocationInitial(self):
        #self.locationOfBS=self.bsLocationInitial()#基站位置初始化
        #self.locationOfUE=self.userLocationInitial()#用户位置初始化
        #测试LocationOfBS、LocationOfUE
        self.locationOfBase = [[0, 0], [0, 100], [100, 0], [100, 100]]  # 基站位置初始化
        self.locationOfUser = [[25, 0], [50, 0], [75, 0], [0, 25], [0, 50], [0, 75], [25, 25], [25, 50],
                             [50, 50]]  # 用户位置初始化
        self.getVQD()#视频描述存储位置初始化
    '''矩阵数据均从下标0就开始存储'''
    '''1.VN矩阵，用户与视频之间的访问关系，会返回生成矩阵，在总的初始化矩阵中再调用这个函数'''
    def VNInitial(self):
        VN = []
        for i in range(0, self.sumOfVideo):
            VN.append([])
            for j in range(0, self.sumOfUser):
                n = random.uniform(0, 10)
                if (n < 4):
                    VN[i].append(-1)
                else:
                    VN[i].append(1)
        return VN
    '''2.生成VQS矩阵，即，每个视频的描述大小,会返回生成的矩阵，在总的初始化矩阵中再调用这个函数'''
    def VQSInitial(self):
        VQS = []
        for i in range(self.sumOfVideo):
            VQS.append([])
            numofdescription = int(random.randint(9, 10))
            j = 0
            while (j < numofdescription):
                sizeOfDescription = random.randint(4, 5)
                VQS[i].append(sizeOfDescription)
                # sum+=sizeOfDescription
                j += 1
        # self.BScapacity=int(sum/self.numofBS)+20
        return VQS
    '''3.基站位置的初始化。基站是4个,整个拓扑，长=宽=500m'''
    def baseLocationInitial(self):
        locationOfBase = [[125, 125], [375, 125], [125, 375], [375, 375]]
        self.width = 500
        self.height = 500
        return locationOfBase
    '''4.用户位置的初始化'''
    def userLocationInitial(self):
        locationOfUser = []
        for i in range(self.sumOfUE):
            x = random.randint(0, 500)
            y = random.randint(0, 500)
            locationOfUser.append([x, y])
        return locationOfUser
    # 需要条件：用户访问视频矩阵，VQS视频的描述大小， 基站分布
    def getVQD(self):#得到三种视频存储位置，顺序存储，随机存储，按照视频重要度，
        self.VQD1=self.getVQD1()#顺序存储
        self.VQD2=self.getVQD2()#随机存储
        self.VQD3=self.getVQD3()#基于视频重要度+距离确定存储位置
        self.VQD4=self.getVQD4()
    def getVQD1(self):#顺序存储，实际是一个三维矩阵，基站+视频+描述
        VQD1=[]
        baseCapacity=copy.deepcopy(self.baseCapacity)#=self.BScapacity #BScapacity=self.BScapacity#标记每个基站的声剩余存储容量
        flagOfBase=0#顺序存储，当前访问到哪个基站，初始化为0基站
        #顺序存储。，基站1-->S,用户1-->V
        for i in range(len(self.VQS)):
            VQD1.append([])
            for j in range(len(self.VQS[i])):#对于视频i的所有描述
                if (baseCapacity[flagOfBase]<self.VQS[i][j]):#当前基站不能存下这个视频
                    flagOfBase += 1
                    if(flagOfBase>=self.sumOfBase):
                        exit("超出所有基站容量，退出")
                        '''
                    print("基站容量大，开始下一个基站")#找出问题所在，超出基站容量
                    print(flag_of_BS)
                    print(i,j)'''
                VQD1[i].append(flagOfBase)  # 在VQD中存储当前描述存储的基站
                baseCapacity[flagOfBase] -= self.VQS[i][j]  # 当前基站的剩余容量=基站容量-视频描述大小
        return VQD1
    def getVQD2(self):#随机存储
        baseCapacity=copy.deepcopy(self.baseCapacity)#self.BScapacity#存储每个基站的容量，以得到VQD2
        VQD2 = []#返回的数据，视频的存储矩阵
        for i in range(len(self.VQS)):#基站
            VQD2.append([])
            for j in range(len(self.VQS[i])):#对于视频i的所第j个描述
                #随机产生一个基站（满足：基站剩余容量能够存储这个描述，否则继续产生一个随机矩阵，直至能够存储下这个描述）
                n=random.randint(0,self.sumOfBase-1)#随机产生一个基站
                while(baseCapacity[n]<self.VQS[i][j]):#如果基站剩余容量不能存储这个视频描述
                    n = random.randint(0, self.sumOfBase - 1) #继续产生一个随机数
                VQD2[i].append(n)  # 在VQD中存储当前描述存储的基站
                baseCapacity[n] -= self.VQS[i][j]  # 当前基站的剩余容量=基站容量-视频描述大小
        return VQD2
    #根据视频的重要度进行排序
    def getVQD3(self):
        VQD3=[]#返回的数据，视频的存储矩阵，第三种存储方式
        baseCapacity=copy.deepcopy(self.baseCapacity)#self.BScapacity#每个基站的存储容量
        '''确认视频存储到哪个基站的距离到所有访问用户的距离最近横-视频video，竖-基站，存储在哪个基站 ，离所有访问用户的距离最近'''
        sorted_Base_Distance=self.getNearestBaseToVideoVisitingUser(self.VN,self.locationOfBase,self.locationOfUser)
        videoImportance=self.getVideoImportance(self.VN)#视频的重要读排序是一个一维数组，基于视频的访问用户多少进行排序
        for i in range(self.sumOfVideo):
            VQD3.append([])
        for i in range(len(videoImportance)):#i:0-->5,视频Video_importance[i]，0 3 1 2视频存储顺序不是按照顺序，而是按照重要度
            flagOfBase=0#从距离最近的基站开始
            video=videoImportance[i]#视频
            for description in range(len(self.VQS[video])):#描述大小VQS[Video_importance[i][description]#访问用户+基站位置--》视频放哪儿合适
                #找到能够存储，且距离最小的基站，1.视频的重要度 2.距离的计算（访问用户到各个基站的总距离）
                videoDescriptionSize=self.VQS[video][description]#描述大小
                flag=0#描述>基站剩余容量
                '''找到能够存这个描述的基站，则直接跳出while循环'''
                while(flag==0):
                    storedBS=sorted_Base_Distance[video][flagOfBase]
                    if(videoDescriptionSize>baseCapacity[storedBS]):
                        flagOfBase+=1
                    else:
                        flag=1
                baseCapacity[storedBS]-=videoDescriptionSize
                VQD3[video].append(storedBS)
        return VQD3

   #需要重新写个VQD初始化，需要考虑
    '''在基站有剩余容量的情况下，视频可以存储几遍，这样命中率就高了'''
    def getVQD4(self):
        VQD=[]#返回的数据，视频的存储位置，第四种方式，比较特殊BScapacity=copy.deepcopy(self.BScapacity)#self.BScapacity#每个基站的存储容量
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#每个基站的存储容量
        '''确认视频存储到哪个基站的距离到所有访问用户的距离最近横-视频video，竖-基站，存储在哪个基站，离所有访问用户的距离最近'''
        nearestBaseDistance = self.getNearestBaseToVideoVisitingUser(self.VN, self.locationOfBase, self.locationOfUser)
        videoImportance = self.getVideoImportance(self.VN)  # 视频的重要读排序是一个一维数组，基于视频的访问用户多少进行排序
        for i in range(self.sumOfVideo):
            VQD.append([])
        for videoFlag in range(len(videoImportance)):  # i:0-->5,视频Video_importance[i]，0 3 1 2视频存储顺序不是按照顺序，而是按照重要度
            flagOfBase = 0  # 从距离最近的基站开始
            video = videoImportance[videoFlag]  # 视频
            for description in range(len(self.VQS[video])):  # 描述大小VQS[Video_importance[i][description]#访问用户+基站位置--》视频放哪儿合适
                # 找到能够存储，且距离最小的基站，1.视频的重要度 2.距离的计算（访问用户到各个基站的总距离）
                VQD[video].append([])
                videoDescriptionSize = self.VQS[video][description]  # 描述大小
                flag = 0  # 描述>基站剩余容量
                '''找到能够存这个描述的基站，则直接跳出while循环'''
                while (flag == 0):
                    storedBS = nearestBaseDistance[video][flagOfBase]
                    if (videoDescriptionSize > baseCapacity[storedBS]):
                        flagOfBase += 1
                    else:
                        flag = 1
                baseCapacity[storedBS] -= videoDescriptionSize
                VQD[video][description].append(storedBS)
        '''之后利用基站的剩余存储容量,重要度高的视频，看看离访问用户最近的基站'''
        for videoFlag in range(len(videoImportance)):
            video=videoImportance[videoFlag]
            for userFlag in range(len(self.VN[video])):
                user=self.VN[video][userFlag]
                if(user==1):#用户user访问视频video
                    i=0
        return VQD

    '''3.1. 根据每个视频的每个访问用户，确认视频存储到哪个基站的距离到所有访问用户的距离最近,GetVQD3函数会调用这个函数'''
    def getNearestBaseToVideoVisitingUser(self, VN, locationOfBase, locationOfUser):#计算每个视频的每个访问用户到哪个基站的距离最近
        minDistance=[]
        distance = []#计算视频访问用户到基站的距离，没有排序
        for video in range(self.sumOfVideo):#视频i 横
            distance.append([])
            for bs in range(self.sumOfBase):#基站j 竖
                distance[video].append([0,bs])#加入基站标识，这样在对距离进行排序时，基站也会自动排序
                for user in range(len(VN[video])):#对于这个视频的所有访问用户k
                    if (VN[video][user] == 1):  # 用户k到基站j的距离
                        currentDistance = ((locationOfBase[bs][0] - locationOfUser[user][0]) ** 2 + (locationOfBase[bs][1] - locationOfUser[user][1]) ** 2) ** 0.5
                        distance[video][bs][0] += currentDistance
        #下面基于得到的距离矩阵Distance，进行排序，计算结果：视频 1-->V ,基站 距离小-->距离大
        ss=[]
        for video in range(len(distance)):#在每一行中，即每个视频中的所有基站，基于距离进行排序（距离+基站标识），是一个三维矩阵
            nn = distance[video]
            nn.sort(key=lambda nn: nn[0])
            ss.append(nn)
        #MinDistance排序后的距离
        for video in range(len(ss)):#对三维矩阵，对于每一个视频，每一行，数据原本是距离+基站标识，抽取出基站标识
            minDistance.append([])
            for bs in range(len(ss[video])):
                minDistance[video].append(ss[video][bs][1])
        return minDistance#返回基于距离排序后，基站的优先存储顺序
    '''3.2. 计算视频的访问用户数量，哪个视频比较重要（越重要，访问用户越多）'''
    def getVideoImportance(self,VN):#根据VN(每个视频的访问用户)，对视频的重要度排序，返回排序后的视频
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
        n=sorted(ns,key=lambda ns:ns[0],reverse=True)
        for i in range(len(n)):
            Sort_Video.append(n[i][1])
        return Sort_Video
    '''4.每个基站的访问用户，Individual个体的初始化，分配基站的信道和功率时使用'''
    def getBaseVisitedUE(self):
        VQD=copy.deepcopy(self.VQD2)
        #去掉列表中的重复元素
        temp_VQD=[]#视频描述的存储位置，去掉列表VQD中的重复元素后的数组
        for i in range (len(VQD)):
            temp_VQD.append([])
            for element in VQD[i]:
                if element not in temp_VQD[i]:
                    temp_VQD[i].append(element)
        basevisitedUE=[]#横坐标i：基站，纵坐标j：用户
        for i in range (self.sumOfBase):#i：基站
            basevisitedUE.append([])
            for j in range (len(temp_VQD)):#视频j，访问用户，没有重复元素
                for k in range(len(temp_VQD[j])):
                    if (temp_VQD[j][k]==i):#当前j视频的第k个描述存储在基站i上，找到这个视频的访问用户
                        for m in range(len(self.VN[j])):
                            if ((self.VN[j][m]!=-1)and (m not in basevisitedUE[i])):
                                basevisitedUE[i].append(m)
            basevisitedUE[i].sort()
        return copy.deepcopy(basevisitedUE)#返回每个基站的访问用户（根据视频描述存储位置+每个视频的访问用户）
        #基于VN（视频访问用户）和VQD
    #1.创建种群
    def creatPopulation(self):#创建种群
        for i in range(Population.sizeOfPopulation):
            n=Individual(self)
            self.individualList.append(n)
    #固定CP分配
    def testInitCP(self):
        self.individualList[0].P = [[10, 10, 10, 9, 9, 10, 11, 10, 10, 9], [9, 10, 10, 10, 10, 9, 9, 11, 11, 10],
                                          [9, 0, 10, 9, 9, 9, 9, 9, 11, 10], [9, 0, 11, 0, 11, 10, 9, 11, 0, 9]]
        self.individualList[0].C = [[3, 6, 8, 0, 2, 3, 6, 0, 7, 3], [4, 6, 8, 3, 6, 8, 3, 0, 2, 3],
                                          [8, -1, 7, 4, 6, 2, 4, 2, 4, 2], [3, -1, 6, -1, 7, 3, 4, 3, -1, 4]]
        self.individualList[1].C = [[-1, -1, -1, 6, 0, 0, 6, 2, 6, 3], [3, 3, 3, 3, 7, 3, -1, 8, 2, 4],
                                          [-1, 8, -1, 8, 6, 2, -1, -1, 7, 2], [-1, 4, 6, 4, 4, 3, 2, -1, 1, 3]]
        self.individualList[1].P = [[0, 0, 0, 10, 10, 9, 9, 11, 10, 10], [10, 9, 11, 11, 9, 11, 0, 10, 9, 9],
                                          [0, 10, 0, 11, 11, 10, 0, 0, 11, 9], [0, 10, 11, 11, 9, 11, 11, 0, 10, 10]]
        self.individualList[2].C = [[3, 3, 7, 0, 8, 8, 6, 0, -1, 3], [1, -1, 6, 6, 2, 7, 4, 7, 2, 7],
                                          [1, -1, -1, 3, 6, 4, 8, -1, 0, 4], [2, 3, 2, -1, 2, 2, 1, 3, 8, -1]]
        self.individualList[2].P = [[10, 11, 11, 11, 10, 10, 11, 9, 0, 9], [9, 0, 10, 9, 10, 9, 10, 9, 9, 10],
                                          [10, 0, 0, 11, 10, 9, 10, 0, 10, 10], [11, 11, 11, 0, 9, 9, 9, 11, 11, 0]]
        self.individualList[3].C = [[6, 3, 0, -1, 8, 2, 7, 3, 6, 2], [1, -1, 3, 1, 7, 2, 3, 2, -1, 2],
                                          [1, -1, -1, 2, -1, 7, -1, 7, 3, -1], [8, -1, 4, -1, -1, 4, 4, 3, 1, -1]]
        self.individualList[3].P = [[11, 9, 9, 0, 11, 11, 10, 11, 10, 9], [9, 0, 10, 9, 10, 10, 9, 10, 0, 9],
                                          [11, 0, 0, 10, 0, 10, 0, 11, 11, 0], [9, 0, 9, 0, 0, 10, 9, 11, 11, 0]]
        self.individualList[4].C = [[6, 3, -1, 6, -1, 7, 6, 3, 8, 8], [7, 1, 0, 0, 8, 6, -1, 1, -1, 3],
                                          [6, 6, 8, 6, 2, -1, -1, 3, 2, 7], [-1, 1, 8, 7, 6, 7, 3, 3, -1, 4]]
        self.individualList[4].P = [[11, 9, 0, 10, 0, 9, 10, 11, 9, 9], [10, 11, 10, 9, 9, 10, 0, 10, 0, 9],
                                          [9, 11, 9, 11, 11, 0, 0, 11, 11, 9], [0, 10, 9, 10, 11, 11, 9, 10, 0, 11]]
        self.individualList[5].C = [[3, 7, 0, 3, 2, -1, -1, 0, -1, 7], [0, 7, 1, 4, 4, -1, -1, 6, 7, 7],
                                          [2, 8, 1, -1, 0, 7, 3, 0, 4, 6], [2, 1, 1, 4, -1, 3, -1, 4, 8, 3]]
        self.individualList[5].P = [[11, 10, 9, 9, 9, 0, 0, 9, 0, 11], [11, 9, 9, 10, 11, 0, 0, 11, 11, 9],
                                          [11, 9, 11, 0, 9, 9, 11, 9, 9, 11], [11, 10, 9, 10, 0, 9, 0, 10, 11, 9]]
        self.individualList[6].C = [[3, 6, 6, 7, 0, 7, 8, 6, 8, 8], [8, 7, 3, 7, 1, 4, 2, 3, 4, 3],
                                          [2, 0, 8, 7, 4, 7, -1, 7, 1, -1], [7, -1, 8, -1, -1, 1, 2, 3, 3, 1]]
        self.individualList[6].P = [[11, 11, 9, 11, 11, 9, 9, 10, 11, 9], [11, 10, 10, 11, 10, 11, 10, 10, 9, 11],
                                          [10, 10, 9, 11, 9, 9, 0, 10, 9, 0], [10, 0, 9, 0, 0, 11, 10, 10, 11, 11]]
        self.individualList[7].C = [[6, 7, -1, -1, 0, 6, 3, 6, -1, 7], [1, 0, 0, -1, 2, 7, 8, 3, 1, 2],
                                          [8, 8, 0, 0, -1, 6, 7, -1, 0, -1], [-1, 2, 4, 1, 6, 7, -1, 4, 2, 7]]
        self.individualList[7].P = [[9, 9, 0, 0, 9, 9, 9, 10, 0, 11], [10, 11, 10, 0, 9, 11, 9, 11, 10, 10],
                                          [9, 9, 9, 10, 0, 10, 9, 0, 11, 0], [0, 9, 11, 9, 11, 10, 0, 10, 11, 10]]
        self.individualList[8].C = [[8, -1, 8, 7, 8, 0, -1, 2, 8, -1], [6, 4, 7, 8, 6, 6, 7, -1, -1, 3],
                                          [7, 4, 2, 1, 8, 8, 8, -1, 3, 2], [6, 2, 1, 6, -1, 4, -1, 4, -1, 6]]
        self.individualList[8].P = [[11, 0, 9, 9, 10, 10, 0, 11, 11, 0], [9, 11, 9, 11, 11, 9, 10, 0, 0, 10],
                                          [10, 11, 11, 9, 10, 10, 10, 0, 11, 11], [10, 11, 11, 10, 0, 11, 0, 11, 0, 10]]
        self.individualList[9].C = [[-1, 2, 6, 6, 0, 8, 3, 2, 7, 2], [8, 2, 2, 8, -1, 4, 0, 2, 3, 7],
                                          [0, 1, -1, 4, 6, 1, 7, -1, -1, 8], [4, 1, 4, -1, -1, 3, 6, 7, 6, -1]]
        self.individualList[9].P = [[0, 10, 10, 10, 10, 10, 10, 10, 9, 10],
                                          [10, 10, 10, 10, 0, 11, 9, 11, 11, 11], [10, 10, 0, 10, 10, 11, 11, 0, 0, 9],
                                          [9, 11, 11, 0, 0, 9, 11, 11, 10, 0]]

    #2.交叉，返回空或者交叉之后的两个新个体，交叉操作已测试成功
    def crossover(self,individualForCross):#individualForCross是一个数组，里面有两个个体individualForCross[0],individualForCross[1]
        if (random.random()<self.crossoverPc):#小于这个概率，执行交叉操作
            individualforMutate=individualForCross[0].crossover(individualForCross[1])#使用个体类自己的方法
        else:#否则，不交叉
            individualforMutate=[]
        return copy.deepcopy(individualforMutate)
    #3.变异，传入参数是两个个体，返回变异之后的两个个体，有可能是原个体，有可能是新的个体
    def mutate(self,individualForMutate):#individualForMutate，自己写，只有一个个体参数
        afterMutate=[]#存储经过变异处理后的个体
        for i in range(2):
            if (random.random()<self.mutatePm):#小于mutatePm，执行变异操作
                afterMutate.append(individualForMutate[i].mutate())
            else:#不执行变异操作，直接将原个体加入
                afterMutate.append(individualForMutate[i])
        return afterMutate
    #4.得到所有个体的适应值
    def getAllFitness(self):
        fitnessList=[]
        for i in range(self.sizeOfPopulation):
            fitnessList.append(self.individualList[i].getFitness())#在individual文件中，这个函数的写法比较重要，好好写
        return copy.deepcopy(fitnessList)
    def select(self):#根据种群适应值，选择两个个体，进行交叉，锦标赛选择法
        #竞争函数
        competitors_1= random.sample(Population.individualList,2)#随机产生两个样本，第一组竞争
        competitors_2= random.sample(Population.individualList,2)#随机产生两个样本，第二组竞争
        fitness_1=[competitors_1[0].getFitness(),competitors_1[1].getFitness()]
        fitness_2=[competitors_2[0].getFitness(),competitors_2[1].getFitness()]
        if(fitness_1[0]<fitness_1[1]):
            father=competitors_1[0]
        else:
            father = competitors_1[1]
        if (fitness_2[0] < fitness_2[1]):
            mather = competitors_2[0]
        else:
            mather = competitors_2[1]
        return [father,mather]
    '''5.修改，对种群中不满足约束条件的个体进行修复，想想怎么写？？？'''
    def revise(self):
        for i in range(self.sizeOfPopulation):
            self.individualList[i].revise()

