import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from math import sqrt
import json
import json

df = pd.read_csv('C:/Users/74024/Documents/study/Going/DM/DM427/youtube-new/USvideos.csv', low_memory=False)

# views五数概括为：549，242329.0，2360784.6382573447，1823157.0，225211923
def views(nums):
    for i in range(len(nums['views'])):
        if((nums['views'][i])<240000):
            nums.loc[i, 'views'] = '<24000'
        elif ((nums['views'][i]) < 1800000):
            nums.loc[i, 'views'] = '[20000,1800000]'
        elif ((nums['views'][i]) < 2400000):
            nums.loc[i, 'views'] = '[1800000,2400000]'
        else:
            nums.loc[i, 'views'] = '>2400000'

# likes五数概括为：0，5424.0，74266.7024347359，55417.0，5613827
def likes(nums):
    for i in range(len(nums['likes'])):
        if ((nums['likes'][i])<5000):
            nums.loc[i, 'likes']  = '<5000'
        elif((nums['likes'][i])<55000):
            nums.loc[i, 'likes'] = '[5000,55000]'
        elif((nums['likes'][i])<75000):
            nums.loc[i, 'likes'] = '[55000,75000]'
        else:
            nums.loc[i, 'likes'] = '>75000'
# dislikes五数概括为：0，202.0，3711.400888910596，1938.0，1674420
def dislikes(nums):
    for i in range(len(nums['dislikes'])):
        if ((nums['dislikes'][i])<200):
            nums.loc[i, 'dislikes']  = '<200'
        elif((nums['dislikes'][i])<2000):
            nums.loc[i, 'dislikes'] = '[200,2000]'
        elif ((nums['dislikes'][i]) < 3700):
            nums.loc[i, 'dislikes'] = '[2000,3700]'
        else:
            nums.loc[i, 'dislikes'] = '>3700'
# comment_count五数概括为：0，614.0，8446.803682629612，5755.0，1361580
def comment(nums):
    for i in range(len(nums['comment_count'])):
        if ((nums['comment_count'][i])<600):
            nums.loc[i, 'comment_count']  = '<600'
        elif((nums['comment_count'][i])<5700):
            nums.loc[i, 'comment_count'] = '[600,5700]'
        elif ((nums['comment_count'][i]) <8400):
            nums.loc[i, 'comment_count'] = '[5700,8400]'
        else:
            nums.loc[i, 'comment_count'] = '>8400'
views(df)
likes(df)
dislikes(df)
comment(df)
df.to_csv("youtube2.csv")



plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
nums=("支持度0.4 置信度0.5","支持度0.4 置信度0.7","支持度0.5 置信度0.5","支持度0.5 置信度0.7",
      "支持度0.6 置信度0.7",
      "支持度0.7 置信度0.7")
sup=[47,47,31,31,7,7]
conf=[30,16,23,11,8,8]
plt.figure(figsize=(12, 7), dpi=98)
# 添加数据标签
for a, b in zip(nums, sup):
    plt.text(a, b + 0.1, '%.0f' % b, ha='center', va='bottom', fontsize=10)
for a, b in zip(nums, conf):
    plt.text(a, b + 0.1, '%.0f' % b, ha='center', va='bottom', fontsize=10)
plt.plot(nums,sup,"-o",label="频繁项集")
plt.plot(nums,conf,"-o",label="关联规则")
plt.ylabel("数目")
plt.title("关联规则挖掘数目比较")
plt.legend()
plt.show()


