# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 14:44:32 2022

@author: mi
"""
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 视图可以显示中文
plt.rcParams['axes.unicode_minus'] = False
# 调节图像大小,清晰度
plt.figure(figsize=(9,6),dpi=150)

data = pd.read_csv('家庭成员信息表5.csv')
df = data.SFZP.value_counts()  
print(df)
orea = ["没有致贫","致贫"]
num = []
for i in df:
    num.append(i)
plt.pie(num,labels=orea,autopct="%1.2f%%")
plt.axis('equal')    #显示为圆(避免压缩为椭圆)
plt.legend(loc="lower left",fontsize="x-small")
plt.show()
