import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
def loadDataSet():
    clean_data = pd.DataFrame(pd.read_csv("youtube2.csv"))
    new_data = []
    # 关联规则挖掘数据处理
    for v in range(1, len(clean_data)):
        item = []
        item.append("category_id" + '='+ str(clean_data.loc[v,'category_id']))
        item.append("comments_disabled" + '='+ str(clean_data.loc[v,'comments_disabled']))
        item.append("ratings_disabled" + '='+ str(clean_data.loc[v,'ratings_disabled']))
        item.append("video_error_or_removed" + '='+ str(clean_data.loc[v,'video_error_or_removed']))
        item.append("views" + '=' + str(clean_data.loc[v, 'views']))
        item.append("likes" + '=' + str(clean_data.loc[v, 'likes']))
        item.append("dislikes" + '=' + str(clean_data.loc[v, 'dislikes']))
        item.append("comment_count" + '=' + str(clean_data.loc[v, 'comment_count']))
        item.append("trending_date" + '=' + str(clean_data.loc[v, 'trending_date']))
        #print(item)
        new_data.append(item)
    print(len(new_data))
    return new_data # [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
def createC1(dataSet):  # 产生单个item的集合
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    return map(frozenset, C1)  # 给C1.list每个元素执行函数


def scanD(D, ck, minSupport):  # dataset,a list of candidate set,最小支持率 支持度计数

    ssCnt = {}
    # temp_D = list(D)
    numItem = float(len(D))
    temp_ck = list(ck)
    for tid in D:
        for can in temp_ck:
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1

    retList = []
    supportData = {}
    for key in ssCnt:
        if numItem == 0:
            continue
        support = ssCnt[key] / numItem
        if support >= minSupport:
            retList.insert(0, key)
            supportData[key] = round(support,3)
    return retList, supportData  # 返回频繁k项集，相应支持度


def aprioriGen(Lk, k):  # create ck(k项集)
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()  # 排序
            if L1 == L2:  # 比较i,j前k-1个项若相同，和合并它俩
                retList.append(Lk[i] | Lk[j])  # 加入新的k项集 | stanf for union
    return retList # ck


def apriori(dataSet, minSupport):
    C1 = createC1(dataSet) # c1 = return map
    # D = map(set, dataSet) # D = map
    D = dataSet
    L1, supportData = scanD(D, C1, minSupport)  # 利用k项集生成频繁k项集（即满足最小支持率的k项集）
    L = [L1]  # L保存所有频繁项集
    k = 2
    while (len(L[k - 2]) > 0):  # 直到频繁k-1项集为空
        Ck = aprioriGen(L[k - 2], k)  # 利用频繁k-1项集 生成k项集
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)  # 保存新的频繁项集与其支持度
        L.append(Lk)  # 保存频繁k项集
        k += 1
    return L, supportData  # 返回所有频繁项集，与其相应的支持率


def calcConf(freqSet, H, supportData, brl, minConf):
    prunedH = []
    lift = []
    file = open("generate_rules.txt","a",encoding = "utf-8")
    for conseq in H:  # 后件中的每个元素
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            file.write(str(freqSet - conseq)+"-->"+str(conseq)+" 支撑度:"+str(supportData[freqSet])+" 置信度:"+str(round(conf,3))+'\n')
            brl.append((freqSet - conseq, conseq, supportData[freqSet], round(conf,3)))  # 添加入规则集中
            prunedH.append(conseq)  # 添加入被修剪过的H中
    file.close()
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf):
    m = len(H[0])  # H是一系列后件长度相同的规则，所以取H0的长度即可
    if (len(freqSet) > m + 1):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


def generateRules(L, supportData, minConf):
    bigRuleList = []  # 存储规则
    rules=[]
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    for i in bigRuleList:
        flag=0
        for j in rules:
            if i[3]==j[3]:
                flag=1
                break
        if i[3]>=minConf:
            if flag==0:
                rules.append(i)
    return rules


def lift_eval(rules, suppData): # lift evaluation
    # lift(A, B) = P(A交B) / (P(A) * P(B)) = P(A) * P(B | A) / (P(A) * P(B)) = P(B | A) / P(B) = confidence(A— > B) / support(B) = confidence(B— > A) / support(A)
    lift = []
    for rule in rules:
        freqSet_conseq = rule[0]
        conseq = rule[1]
        lift_val = round(float(rule[3]) / float(suppData[rule[1]]),3)
        lift.append([freqSet_conseq,conseq,rule[2],rule[3],lift_val])
    return lift

def kulc(rules, suppData):
    print()
    kulc_score = []
    for rule in rules:
        num = float(rule[2])
        freqSet_conseq = suppData[rule[0]]
        conseq = suppData[rule[1]]
        first_pro = num / freqSet_conseq
        second_pro = num / conseq
        kulc = round((first_pro + second_pro) / 2,3)
        kulc_score.append([rule[0],rule[1],num,rule[3],rule[4],kulc])
    return  kulc_score;

def li_ku(n,lift_score,kulc_score):
    x = np.arange(1,n+1)  # 点的横坐标
    k1 = lift_score  # lift纵坐标
    k2 = kulc_score  # kulc的纵坐标
    plt.plot(x, k1, 's-', color='plum', label="Lift")  # s-:方形
    plt.plot(x, k2, 'o-', color='slateblue', label="Kulc")  # o-:圆形
    plt.xlabel("2-items")  # 横坐标名字
    plt.ylabel("score")  # 纵坐标名字
    plt.legend(loc="best")  # 图例
    plt.title("Rule evaluation chart")
    plt.show()

def su_co(n,support,confidence):
    x =  np.arange(1,n+1) # 点的横坐标
    k1 = support  # 支持度的纵坐标
    k2 = confidence  # 置信度的纵坐标
    plt.plot(x, k1, 's-', color='dodgerblue', label="support")  # s-:方形
    plt.plot(x, k2, 'o-', color='teal', label="confidence")  # o-:圆形
    plt.xlabel("2-items")  # 横坐标名字
    plt.ylabel("score")  # 纵坐标名字
    plt.legend(loc="best")  # 图例
    plt.title("support-confidence chart")
    plt.show()

dataSet = loadDataSet()
L, suppData = apriori(dataSet,0.4)
print("频繁项集：")
print(len(suppData))
for key,value in suppData.items():
    print("{}，支持度：{}".format(key,value))
rules = generateRules(L, suppData, 0.7)
print("关联规则：")
print(len(rules))
# for i in rules:
#     print("{}—>{}，置信度：{}".format(i[0],i[1],i[3]))
lifts = lift_eval(rules, suppData)
kf=kulc(lifts, suppData)
li=[]
ku=[]
sup=[]
conf=[]
num=0
for i in kf:
    num=num+1
    print("({}){}—>{}".format(num,i[0], i[1]))
    print("支持度：{}，置信度：{}，lift评价：{}，kulc评价：{}".format(i[2],i[3],i[4],i[5]))
    li.append(i[4])
    ku.append(i[5])
    sup.append(i[2])
    conf.append(i[3])
# print(lifts)
li_ku(num,li,ku)
su_co(num,sup,conf)