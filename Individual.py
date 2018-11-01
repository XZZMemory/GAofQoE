import  random
import copy
class Individual:
    #定义高斯白噪声
    Ti=9.56#包丢失率的阈值 9.56db
    averagePower_dbm=40# 分贝毫瓦
    averagePower=10**((averagePower_dbm-30)/10)#瓦
    def __init__(self,population):#初始化的时候加上population.方便传输参数
        i=0
        #（--------以下均是拷贝种群参数信息------已测试，信息均可以传输
        self.LocationOfBS=copy.deepcopy(population.LocationOfBS)#拷贝基站和用户的坐标位置
        self.LocationOfUE =copy.deepcopy(population.LocationOfUE)
        self.sumofBS=population.sumofBS
        self.sumOfUE=population.sumOfUE
        self.sumOfVideo=population.sumOfVideo
        self.sumofchannels=population.sumofchannels
        self.VN=population.VN
        #--------拷贝种群信息结束-----------）
        self.C=[]# 信道分配矩阵
        self.P=[]#功率分配矩阵
        self.BasevisitedUE=population.BasevisitedUE#每个基站的访问用户
        self.initialOfCandP()
        self.DistanceUEToBase=self.GetDistanceUEToBase()#计算用户与基站之间的距离，用于计算SINR
        self.VQD2=population.VQD2#视频V的第q个描述的存储地点
        # 得到基站到用户的距离
    def GetDistanceUEToBase(self):
        Distance = []
        for i in range(self.sumOfUE):  # 求所有用户到基站的距离 用户i横坐标
            Distance.append([])
            for j in range(self.sumofBS):  # 基站j 竖坐标
                n=((self.LocationOfUE[i][0]-self.LocationOfBS[j][0])**2+(self.LocationOfUE[i][1]-self.LocationOfBS[j][1])**2)**0.5
                Distance[i].append(n)

    '''
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
            '''
    '''1.信道和功率的初始化，需要改改，2018.6.11，信道和功率的分配需要考虑实际情况，只有用户访问基站时，在初始化时，才会分配信道，
       用户不访问基站时，不分配信道，在交叉和变异的过程中，会发生变化，不满足这个条件，需要进行修正，参考洪庭贺毕设中关于修正的部分，后续需要进行修正
    '''
    def initialOfCandP(self):
        for i in range(self.sumofBS):
            self.C.append([])
            self.P.append([])
            for j in range(self.sumofchannels):#信道分配给哪个用户传输,这个信道分配的功率是多少
                #信道分配给哪个用户进行传输数据，得到每个基站的访问用户
                #n=random.randint(-1,self.sumOfUE),信道分配，-1代表不分配给用户，横坐标，基站，纵坐标，用户
                p=random.random()
                if((p<0.8)and(len(self.BasevisitedUE[i])!=0)):#信道分配用户
                    f = random.sample(self.BasevisitedUE[i],1)[0]#random.sample()从指定的序列中随机截取指定长度的片段，不作原地修改，返回的仍是列表，不是一个单独数字
                    self.C[i].append(f)
                    self.P[i].append((random.randint(9, 11)))
                else :#信道不分配
                    self.C[i].append(-1)# 信道不分配给用户，所以功率为0
                    self.P[i].append(0)
                '''
                print("输出C")
                print(C)
                print("输出C结束")
                print("输出P")
                print(P)
                print("输出P结束")'''
                '''交叉变异均是对个体的行为'''
    #2.交叉
    def crossover(self,Individual2):#交叉
        '''从种群中随机选择两个个体，从基站1到S循环，每层产生一个随机数，对应位置交换位置，即交换两个个体的值
        #这是随机选择一个位置交换'''
        child1=copy.deepcopy(self)#深复制，浅复制
        child2=copy.deepcopy(Individual2)
        #交叉两个个体的功率和信道分配
        for i in range(self.sumofBS):#对每一行，随机产生一个变异位，要变异到所有的基站
            print("对于基站")
            print(i)
            m=random.randint(0,self.sumofchannels-1)#随机产生一个交叉位置
            print("交叉位置")
            print(m)
            child2.C[i][m]=self.C[i][m]
            child2.P[i][m]=self.P[i][m]
            child1.P[i][m]=Individual2.P[i][m]
            child1.C[i][m]=Individual2.C[i][m]
        return ([child1,child2])
    #3.变异
    def mutate(self):#变异，一个个体的变异
        '''变异，在种群中选择一个个体，从基站1到S循环，每层产生一个随机数，有对应值删除，无对应值随机分配信道。
        # 随 机选择一个位置进行变异'''
        self_copy=copy.deepcopy(self)
        for i in range(self.sumofBS):#基站
            print("基站")
            print(i)
            j=random.randint(0,self_copy.sumofchannels-1)#随机产生一个数字，列
            print("随机产生的信道")
            print(j)
            if(self_copy.C[i][j]==-1):#这个信道没有分配给任何用户，处于闲置状态
                usernum=random.randint(0,self_copy.sumOfUE-1)
                print("随机产生一个用户，将该信道分配给用户")
                print(usernum)
                self_copy.C[i][j]=usernum#把信道随机分配给一个用户
                print("随机产生一个功率，将该功率分配给信道j")
                Pnum=random.randint(9,11)
                print(Pnum)
                self_copy.P[i][j]=Pnum
            else:#非闲置状态
                print("信道处于非闲置状态")
                p=random.random()#再产生一个随机数
                print("产生一个随机数，小于0.5则将信道置空，否则，随机产生一个用户将该信道分配给用户")
                print(p)
                if(p<0.5):#将该信道置空
                    print("概率p小于0.5，信道功率置空")
                    self_copy.C[i][j]=-1
                    self_copy.P[i][j]=0
                else:#随机选择一个用户，将信道分配给该用户
                    print("概率p大于0.5，随机选择一个用户，将信道、功率分配给用户")
                    usernum = random.randint(0, self.sumOfUE-1)
                    print("随机产生一个用户，将该信道分配给用户")
                    print(usernum)
                    self_copy.C[i][j] = usernum  # 把信道随机分配给一个用户
                    print("随机产生一个功率，将该功率分配给信道j")
                    Pnum = random.randint(9, 11)
                    print(Pnum)
                    self_copy.P[i][j] = Pnum
        print("在individual文件中输出返回值self_copy信道分配+功率分配")
        for i in range(len(self_copy.C)):
            print(self_copy.C[i])
        for i in range(len(self_copy.P)):
            print(self_copy.P[i])
        return self_copy
    '''5.判断个体是否满足约束条件，不满足的话对个体进行修复'''
    def IndividualRevise(self):
        i=0
        '''计算适应值，仔细理解，看看怎么处理数据'''
    def getFitness(self,population):#先计算单个个体的适应值，对于所有的视频，求视频传输质量
        '''SINR  信号与干扰加噪声比
        SINR=[]#S/(I+N)，也是一个数组，每个基站的信道都分配给了一个用户，我们就计算每个信道在分配给该用户的情况下，每个信道的信噪比
        计算SINR，计算PER，计算传输质量，一个个体，C和P，计算传输质量
        计算每个信道的信噪比
        G功率增益模型Gn,k
        计算所有基站，所有信道的信噪比'''
        for i in range(population.sumofBS):#对于所有的基站i
            SINR.append([])
            for j in range(population.sumofchannels):#对于基站i里的所有的信道j，计算信噪比，每个信道的信噪比
                user=self.C[i][j]#信道分配的用户user
                if(user==-1):#信道没有分配给任何用户
                    j=0
                else:#信道分配了，则需要计算SINR
                    # 计算信道功率增益
                    G = self.DistanceUEToBase[user][i] ** (-4)#功率增益模型，基站到用户的距离
                    S=self.P[i][j]*G#在用户k处能接受到的信号强度,信道功率×功率增益
                    I=0#干扰
                    for k in range(self.sumofBS):
                        if((k!=i)and(self.C[k][j]!=-1)):#如果不是当前基站，且基站信道分配给了用户，即功率不是0
                            GOther=self.DistanceUEToBase[user][k]**(-4)#其他基站在用户user处的信道增益
                            Ik=self.P[k][j]*GOther
                            I+=Ik#干扰相加，得到总的干扰
                    N=0#噪声
                    sinr=S/(I)
                    SINR[i].append(sinr)
                    #此处得到来自其他基站的干扰
                    #噪声，采用高斯白噪声
        #计算用户n使用基站n的信道m访问基站n中的视频v的描述q的误码率
         #每个视频描述的误码率
        Pijq=[]#误码率，是一个数组，只要用户访问这个视频了，就需要计算对于这个用户来说，整个视频描述的误码率
        for i in range(len(self.VN)):#视频i
            Pijq.append([])
            for j in range(len(self.VN[i])):#用户j
                Pijq[i].append("????")
                if(self.VN[i][j]==1):#代表这个用户访问这个视频了，需要计算失真emmm，此时需要计算误码率
                    for k in range(len(self.VQD2[i])):#找到视频的存储基站k
                        i=0




        #在VQD1的情况下计算视频传输质量
        #计算误码率








