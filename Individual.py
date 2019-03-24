import  random
import copy
import math
import numpy as np
class Individual:
    #定义高斯白噪声，查查怎么写？？
    BW=1e-7
    dBTi=9.56#包丢失率的阈值 9.56db
    Ti=10**(dBTi/10)
    averagePower_dbm=40# 分贝毫瓦,可用作电压或功率单位
    averagePower=10**((averagePower_dbm-30)/10)#瓦
    ei=1#包大小相关的约束，计算PER使用
    fi=1
    population=[]
    '''个体中需要用到的：1.C、P的初始化 
                        2.个体的适应值计算-不造对不对
                        3.交叉 child1.crossover(child2)  return ([child1,child2])
                        4.变异 child.mutate return copyChild
                        修改:需要在初始化的时候，基站有剩余的存储容量，要存储多的视频，多存几遍视频'''
    def __init__(self,population,typeOfVQD):#初始化的时候加上population.方便传输参数
        i=0
        self.population=population
        #（--------以下均是拷贝种群参数信息------已测试，信息均可以传输
        self.locationOfBase=copy.deepcopy(population.locationOfBase)#拷贝基站和用户的坐标位置
        self.locationOfUser =copy.deepcopy(population.locationOfUser)
        self.sumOfBase=population.sumOfBase
        self.sumOfUser=population.sumOfUser
        self.sumOfVideo=population.sumOfVideo
        self.sumOfChannels=population.sumOfChannels
        self.VN=population.VN
        self.basevisitedUE=population.basevisitedUE#每个基站的访问用户，在个体初始化C、P时使用
        self.VQD = population.VQD # 视频V的第q个描述的存储地点
        self.typeOfVQD=typeOfVQD#视频的存储方式
        if (self.typeOfVQD == 4):
            self.baseVisitedOfUserVisitingVideo =population.baseVisitedOfUserVisitingVideo
        #--------拷贝种群信息结束-----------）
        self.C=[]# 信道分配矩阵
        self.P=[]#功率分配矩阵
        self.initialOfCandP()
        self.distanceUserToBase=self.getDistanceUserToBase()#计算用户与基站之间的距离，用于计算SINR
        self.SINR=[]#信噪比
        # 得到基站到用户的距离-方便计算SINR
    def getDistanceUserToBase(self):
        distance = []
        for i in range(self.sumOfUser):  # 求所有用户到基站的距离 用户i横坐标
            distance.append([])
            for j in range(self.sumOfBase):  # 基站j 竖坐标
                n=((self.locationOfUser[i][0]-self.locationOfBase[j][0])**2+(self.locationOfUser[i][1]-self.locationOfBase[j][1])**2)**0.5
                distance[i].append((int)(n))
        return distance

    '''1.信道和功率的初始化，需要改改，2018.6.11，信道和功率的分配需要考虑实际情况，
         只有用户访问基站时，在初始化时，才会分配信道，用户不访问基站时，不分配信道
             信道初始化已完成
       2.在交叉和变异的过程中，会发生变化，不满足这个条件，需要进行修正，参考洪庭贺毕设
         中关于修正的部分，后续需要进行修正？？
    '''
    def initialOfCandP(self):
        for base in range(self.sumOfBase):#基站i，信道j
            self.C.append([])
            self.P.append([])
            for channel in range(self.sumOfChannels):#信道分配给哪个用户传输,这个信道分配的功率是多少
                p=random.random()
                if((p<0.8)and(len(self.basevisitedUE[base])!=0)):#信道分配用户
                    #从基站的访问用户中随机选择一个用户分配信道
                    user = random.sample(self.basevisitedUE[base],1)[0]#random.sample()从指定的序列中随机截取指定长度的片段，不作原地修改，返回的仍是列表，不是一个单独数字
                    self.C[base].append(user)
                    self.P[base].append((random.randint(6, 11)))
                else :#信道不分配
                    self.C[base].append(-1)# 信道不分配给用户，所以功率为0
                    self.P[base].append(0)
    #2.交叉
    def crossover(self,Individual2):#交叉
        '''从种群中随机选择两个个体，从基站1到S循环，每层产生一个随机数，对应位置交换位置，即交换两个个体的值
        #这是随机选择一个位置交换'''
        child1=copy.deepcopy(self)#深复制，浅复制
        child2=copy.deepcopy(Individual2)
        #交叉两个个体的功率和信道分配
        for i in range(self.sumOfBase):#对每一行，随机产生一个变异位，要变异到所有的基站
            m=random.randint(0,self.sumOfChannels-1)#随机产生一个交叉位置
            child2.C[i][m]=self.C[i][m]
            child2.P[i][m]=self.P[i][m]
            child1.P[i][m]=Individual2.P[i][m]
            child1.C[i][m]=Individual2.C[i][m]
        return ([child1,child2])
    #3.变异，变异通过
    def mutate(self):#变异，一个个体的变异
        '''变异，在种群中选择一个个体，从基站1到S循环i，每层产生一个随机数j,信道j，有对应值删除，无对应值随机分配信道。
        # 随 机选择一个位置进行变异'''
        self_copy=copy.deepcopy(self)
        for base in range(self.sumOfBase):#基站i
            if(len(self.basevisitedUE[base])>0):
                channel = random.randint(0, self_copy.sumOfChannels - 1)  # 随机产生一个基站i的信道j，列
                if (self_copy.C[base][channel] == -1):  # 闲置状态，信道没有分配给任何用户
                    # 随机产生一个用户，将该基站j的信道j分配给用户usernum
                    user = (random.sample(self.basevisitedUE[base], 1))[
                        0]  # random.sample()从指定的序列中随机截取指定长度的片段，不作原地修改，返回的仍是列表，不是一个单独数字
                    self_copy.C[base][channel] = user  # 把信道随机分配给一个用户
                    self_copy.P[base][channel] = random.randint(9, 11)  # 随机产生一个功率
                else:  # 非闲置状态
                    p = random.random()  # 产生一个随机数
                    if (p < 0.5):  # 概率p小于0.5，该信道置空
                        self_copy.C[base][channel] = -1
                        self_copy.P[base][channel] = 0
                    else:  # 概率p大于0.5，随机选择一个用户，将信道、功率分配给该用户
                        self_copy.C[base][channel] = random.sample(self.basevisitedUE[base], 1)[
                            0]  # random.sample()从指定的序列中随机截取指定长度的片段，不作原地修改，返回的仍是列表，不是一个单独数字
                        self_copy.P[base][channel] = random.randint(9, 11)
        return self_copy

        '''计算适应值，仔细理解，看看怎么处理数据'''
    def getFitness(self):#计算单个个体的适应值（对于所有的视频，求视频传输质量）
        self.SINR=self.getSINR()
        self.userList=[0 for i in range(self.sumOfUser)]#用户占用信道数列表，初始化0
        #计算用户n使用基站n的信道m访问基站n中的视频v的描述q的误码率
         #每个视频描述的误码率
        PER=[]#误码率，是一个数组，只要用户访问这个视频了，就需要计算对于这个用户来说，整个视频描述的误码率
        for video in range(len(self.VN)):#视频i
            PER.append([])
            for user in range(len(self.VN[video])):#用户j
                if(self.typeOfVQD==4):
                    PER[video].append(self.getPEROfVQD4(user, video))  # 用户不访问视频，误码率为0.用户访问视频，误码率为0-1
                else:
                    PER[video].append(self.getPEROfVQD123(user, video))  # 用户不访问视频，误码率为0.用户访问视频，误码率为0-1

        fitness=0
        for video in range (len(PER)):
            for user in range(len(PER[video])):
                fitness+=PER[video][user]
        #fitness即所有用户访问视频的误码率，fitness越小越好
        return fitness
    def getPEROfVQD123(self, user, video):#user访问视频video的误码率
        Pnv=1
        if self.VN[video][user]==1:#代表这个用户访问这个视频了，需要计算失真
            for base in self.VQD[video]:#找到视频video的存储基站，到存储基站中找到信道误码率,有多个描述
                Pnvq=1#video的第q个描述，在同一基站使用多条信道，考虑频谱聚合技术
                Pnms=1
                for channel in range(len(self.P[base])):
                    if self.C[base][channel]==user:
                        if self.SINR[base][channel]>self.Ti:#如果sinr大于sinr的门限值，用公式误码率，如果小于则误码率直接为1
                            Pnms = self.ei * math.e ** (-(self.fi * self.SINR[base][channel]))  # 基站s使用信道m给用户n传输数据 ei、fi包大小相关约束
                            Pnvq*=Pnms#频谱聚合技术
                Pnv*=Pnvq#多个描述，每个描述都要求误码率
        else:
            Pnv=0
        return Pnv
    def getPEROfVQD4(self, user, video):#user访问视频video的误码率
        Pnv=1
        self.baseVisitedOfUserVisitingVideo#用户-视频-描述
        if self.VN[video][user]==1:#代表这个用户访问这个视频了，需要计算失真
            for decsription in range(len(self.VQD[video])):#找user访问video的描述description时，访问的基站，去哪个基站找这个视频
                visitedBase=(np.array(self.baseVisitedOfUserVisitingVideo))[user][video][decsription]
                Pnvq = 1  # video的第q个描述，在同一基站使用多条信道，考虑频谱聚合技术
                Pnms = 1
                for channel in range(len(self.P[visitedBase])):
                    if self.C[visitedBase][channel] == user:
                        if self.SINR[visitedBase][channel] > self.Ti:  # 如果sinr大于sinr的门限值，用公式误码率，如果小于则误码率直接为1
                            Pnms = self.ei * math.e ** (
                                -(self.fi * self.SINR[visitedBase][channel]))  # 基站s使用信道m给用户n传输数据 ei、fi包大小相关约束
                            Pnvq *= Pnms  # 频谱聚合技术
                Pnv *= Pnvq  # 多个描述，每个描述都要求误码率

        else:
            Pnv=0
        return Pnv
    def getSINR(self):
        SINR=[]
        for s in range(self.sumOfBase):#对于所有的基站s
            SINR.append([])
            for m in range(self.sumOfChannels):#对于基站s里的所有的信道m，计算信噪比，每个信道的信噪比
                user=self.C[s][m]#信道分配的用户user
                if(user==-1):#信道没有分配给任何用户
                    sinr=-1#sinr=-1代表该信道没有分配给任何用户
                else:#信道分配了，则需要计算SINR
                    # 计算信道功率增益
                    G = self.distanceUserToBase[user][s] ** (-4)#功率增益模型，基站到用户的距离
                    S=self.P[s][m]*G#在用户k处能接受到的信号强度,信道功率×功率增益
                    I=0#干扰计算当前基站s信道m来自其他基站的干扰
                    for ss in range(self.sumOfBase):
                        if((ss!=s)and(self.C[ss][m]!=-1)):#如果不是当前基站，且基站信道处于非闲置状态，即功率不是0
                            GOther=self.distanceUserToBase[user][ss]**(-4)#其他基站在用户user处的信道增益
                            Ik=self.P[ss][m]*GOther
                            I+=Ik#干扰相加，得到总的干扰 # 此处得到来自其他基站的干扰
                    sinr=S/(I+self.BW)# 噪声，采用高斯白噪声BW
                SINR[s].append(round(sinr,9))
        return SINR








