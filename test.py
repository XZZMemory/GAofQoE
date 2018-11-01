from Population import Population
population=Population()
population.Initialization()
#population.creatPopulation()
print("输出VN")
for i in range(len(population.VN)):
    print(population.VN[i])
print("输出VQS")
for i in range(len(population.VQS)):
    print(population.VQS[i])
#population.all_locationInitial()
print(population.LocationOfBS)
for i in range(len(population.LocationOfUE)):
    print(population.LocationOfUE[i])
print("--------------------------测试-------------")
population.creatPopulation()
print("在test函数中输出创建信道+功率分配")
for i in range(len(population.individualList)):
    print(i)
    for j in range(len(population.individualList[i].C)):
        print(population.individualList[i].C[j])
    for j in range(len(population.individualList[i].P)):
        print(population.individualList[i].P[j])
print("25,信道分配+功率分配")
for i in range(len(population.individualList[25].C)):
    print(population.individualList[25].C[i])
for i in range(len(population.individualList[25].P)):
    print(population.individualList[25].P[i])
print("35,信道分配+功率分配")
for i in range(len(population.individualList[35].C)):
    print(population.individualList[35].C[i])
for i in range(len(population.individualList[35].P)):
    print(population.individualList[35].P[i])
print("---------以下进行交叉操作---------")
individualforCross=[]
individualforCross.append(population.individualList[25])
individualforCross.append(population.individualList[35])
after=population.crossover(individualforCross)
'''
after=population.individualList[25].crossover(population.individualList[35])#进行交叉操作'''
print("35,信道分配+功率分配")
for i in range(len(population.individualList[35].C)):
    print(population.individualList[35].C[i])
for i in range(len(population.individualList[35].P)):
    print(population.individualList[35].P[i])
print("25,信道分配+功率分配")
for i in range(len(after[0].C)):
    print(after[0].C[i])
for i in range(len(after[0].P)):
    print(after[0].P[i])
print("35,信道分配+功率分配")
for i in range(len(after[1].C)):
    print(after[1].C[i])
for i in range(len(after[1].P)):
    print(after[1].P[i])
print("---------以下进行变异操作，通过individual文件---------")
aftermutateindivisual=population.individualList[35].mutate()
print("变异后的个体35的信道分配+功率分配")
for i in range(len(aftermutateindivisual.C)):
    print(aftermutateindivisual.C[i])
for i in range(len(aftermutateindivisual.P)):
    print(aftermutateindivisual.P[i])
print("---------以下进行变异操作，通过population文件---------")
individualforMutate=[]
individualforMutate.append(population.individualList[20])
individualforMutate.append(population.individualList[30])
print("变异操作之前的信道+功率分配")
for k in range(2):
    print(k)
    for i in range(len(individualforMutate[k].C)):
        print(individualforMutate[k].C[i])
    for i in range(len(individualforMutate[k].P)):
        print(individualforMutate[k].P[i])
aa=population.mutate(individualforMutate)
print("在test文件中输出变异后的个体20和个体30的信道分配+功率分配")
for k in range(2):
    print(k)
    for i in range(len(aa[k].C)):
        print(aa[k].C[i])
    for i in range(len(aa[k].P)):
        print(aa[k].P[i])
