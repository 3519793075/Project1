# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 09:10:33 2022

@author: mi
"""
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 视图可以显示中文
plt.rcParams['axes.unicode_minus'] = False
# import numpy as np

pd.set_option('display.max_columns', 8)
pd.set_option('display.max_rows', 200)  # 设置最大可见100行

# ------------------------------------------------------------#
# #计算致贫率
# data_JTXX = pd.read_csv('T_XCZXJ_JTXX.csv')
# data_JTXX_clean = data_JTXX.dropna(axis=0, how='any')#去除家庭信息表中ZPYY(致贫原因)为空的行

# print(len(data_JTXX_clean)/len(data_JTXX))

# --------------------------1---------------------------------#
# 在家庭信息表新添加个属性SFZP是否致贫。从家庭信息T_XCZXJ_JTXX表中提取出
# 有致贫原因的那一行，获取那个家庭的ID，然后遍历家庭成员信息T_XCZXJ_JTCYXX表
# 判断是否为致贫的家庭成员，如果是则将该成员的SFZP置为1，否则为0
# data_JTXX = pd.read_csv('T_XCZXJ_JTXX.csv')
# data_JTXX_clean = data_JTXX.dropna(axis=0, how='any')#去除家庭信息表中ZPYY(致贫原因)为空的行
# list = data_JTXX_clean.iloc[:,0]

# data_JTCYXX = pd.read_csv('T_XCZXJ_JTCYXX.csv')
# data_JTCYXX['SFZP'] = 0      #增加一列‘是否致贫’
# for index,row in data_JTCYXX.iterrows():
#     if row['JTXX_ID'] in list.values.tolist():
#         row['SFZP'] = 1
#         data_JTCYXX.iloc[index] = row
# data_JTCYXX.to_csv("家庭成员信息表.csv")
# ------------------------------------------------------------#

# #去除不需要的列
# data = pd.read_csv("家庭成员信息表.csv")
# data = data.drop(columns=['Unnamed: 0','MEMBER_ID','CYSFZ','YHZGX'])#删除指定列
# #data.to_csv("家庭成员信息表1.csv")
# #将致残等级改为数字
# for index,row in data.iterrows():
#     if row['CJDJ'] == '四级':
#         row['CJDJ'] = 4
#         data.iloc[index] = row
#     elif row['CJDJ'] == '三级':
#         row['CJDJ'] = 3
#         data.iloc[index] = row
#     elif row['CJDJ'] == '二级':
#         row['CJDJ'] = 2
#         data.iloc[index] = row
#     elif row['CJDJ'] == '一级':
#         row['CJDJ'] = 1
#         data.iloc[index] = row
#     else:
#         row['CJDJ'] = 0
#         data.iloc[index] = row
# data.to_csv("家庭成员信息表2.csv")

# -----------------------------------------------------------#
# #去除不需要的列，并将空值置为0或1,并将数据按JTXX_ID排序写入表中
# data = pd.read_csv("家庭成员信息表2.csv")

# data = data.drop(columns=['Unnamed: 0','CYXM','WHCD'])#删除指定列
# data['ZXSZK'].fillna(0, inplace=True) #将空值用0填充
# data['CJLB'].fillna(0, inplace=True) #将空值用0填充
# data['JKZK'].fillna(1, inplace=True) #将空值用1填充
# for index,row in data.iterrows():
#     if row['JKZK'] in ['01','02','03','04']:
#         continue
#     else:
#         row['JKZK'] = '4'
#         data.iloc[index] = row
# data['JKZK'] = data['JKZK'].astype(int)
# data_sort = data.sort_values(by='JTXX_ID', ascending=True)
# data_sort.to_csv("家庭成员信息表3.csv")

# -------------------------------------------------------------#

# -------------------------------------------------------------#
# 将一个家庭的人的各项数据相加起来合并为一条数据
#
data = pd.read_csv('家庭成员信息表3.csv')
JTXX_ID = data['JTXX_ID']
data = data.groupby(by='JTXX_ID')
df = pd.DataFrame(columns=['JTXX_ID', 'ZXSZK', 'JKZK', 'CJDJ', 'CJLB', 'LDJN', 'SFSW', 'SFZP'])
JTXX_ID = []
ZXSZK = []
JKZK = []
CJDJ = []
CJLB = []
LDJN = []
SFSW = []
SFZP = []
for key, value in data:
    ZXSZK.append(value['ZXSZK'].sum())
    JKZK.append(value['JKZK'].sum())
    CJDJ.append(value['CJDJ'].sum())
    CJLB.append(value['CJLB'].sum())
    LDJN.append(value['LDJN'].sum())
    SFSW.append(value['SFSW'].sum())
    SFZP.append(value['SFZP'].sum())
    # JTXX_ID.append(value['JTXX_ID'].value)
# JTXX_ID = data['JTXX_ID']
JTXX_ID = sorted(JTXX_ID)
new_JTXX_ID = []
for i in JTXX_ID:
    if i not in new_JTXX_ID:
        new_JTXX_ID.append(i)
df['JTXX_ID'] = pd.Series(new_JTXX_ID)
df['ZXSZK'] = pd.Series(ZXSZK)
df['JKZK'] = pd.Series(JKZK)
df['CJDJ'] = pd.Series(CJDJ)
df['CJLB'] = pd.Series(CJLB)
df['LDJN'] = pd.Series(LDJN)
df['SFSW'] = pd.Series(SFSW)
df['SFZP'] = pd.Series(SFZP)

df.to_csv("家庭成员信息表4.csv")

# -------------------------------------------------------------#

# #将家庭成员信息表4.csv表中的SFZP列不为0的都置为1
# data = pd.read_csv('家庭成员信息表4.csv')
# for index,row in data.iterrows():
#     if row['SFZP'] != 0:
#         row['SFZP'] = 1
#         data.iloc[index] = row
#     else:
#         continue
# # data = data.drop(columns=['Unnamed: 0'])#删除指定列
# data.to_csv('家庭成员信息表5.csv')


# -------------------------------------------------------------#
# #数据探索
# datafile = '家庭成员信息.csv'   #原始数据
# resultfile = 'explore.csv'   #数据探索结果表
# data = pd.read_csv(datafile,encoding='utf-8')

# explore = data.describe(percentiles = [],include = 'all').T

# explore['null'] = len(data) - explore['count']

# explore = explore[['null','top','freq']]
# explore.columns = [u'空值数',u'频数最高者',u'最高频数']  #重命名表头

# explore.to_csv(resultfile)


# 个人自付金额箱线图
# data_YBXJHXX = pd.read_csv('T_XCZXJ_YBSJXX.csv', usecols=['XM', 'SFZH', 'GRZF'])
# plt.boxplot(data_YBXJHXX["GRZF"])
# plt.title("个人自付金额")
# plt.ylabel("金额")
# plt.show()
#
# # 计算上四分位数
# Q1 = data_YBXJHXX.GRZF.quantile(q=0.25)
# Q3 = data_YBXJHXX.GRZF.quantile(q=0.75)
# high_quantile = Q3 + 1.5 * (Q3 - Q1)
# print(high_quantile)
