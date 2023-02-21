# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 15:57:15 2022

@author: mi
"""
import pandas as pd
from sklearn.linear_model import LogisticRegression as LR
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("家庭成员信息表5.csv")

x = data.iloc[:, 1:7].values  # 获取表中前八列的数据
y = data.iloc[:, 7].values  # 读取违约那一列的数据

# 将数据集分为训练集和测试集
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0, test_size=0.25)
# 特征缩放
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

# fit_transform()先拟合数据，再标准化
x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

# lr = LR()  # 建立逻辑回归模型
# lr.fit(x_train, y_train)  # 用筛选后的特征数据来训练模型
#
# print('逻辑回归模型的平均准确度为: %s' % lr.score(x_test, y_test))
# print('模型的平均准确度为: %s' % lr.score(x_train, y_train))

from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline

# PCA主成分分析，在做特征筛选的时候会经常用到，但是，PCA并不是简单的剔除掉一些特征，
# 而是将现有的特征进行一些变换，选择最能表达该数据集的最好的几个特征来达到降维目的
# n_components保留下来的特征个数,whiten是否白化，使得每个特征具有相同的方差
pca = PCA(n_components=3, whiten=True, random_state=42)
# SVC用于分类，kernel='linear'使用线性核函数，C越大，即对分错样本的惩罚程度越大，因此在训练样本中准确率越高，但是泛化能力降低，
# 也就是对测试数据的分类准确率降低。相反，减小C的话，容许训练样本中有一些误分类错误样本，泛化能力强。
# 对于训练样本带有噪声的情况，一般采用后者，把训练样本集中错误分类的样本作为噪声。class_weight考虑类不平衡，类似于代价敏感
svc = SVC(C=1, kernel='linear', class_weight='balanced')
# svc = SVC(C=1, kernel='RBF', class_weight='balanced')
# make_pipeline是一个构造pipeline的简短工具，他接受可变数量的estimators(所使用的分类器)并返回一个pipeline，每个estimator的名称自动填充
model = make_pipeline(pca, svc)

# 调参:通过交叉验证寻找最佳的 C (控制间隔的大小)
from sklearn.model_selection import GridSearchCV

# GridSearchCV，它存在的意义就是自动调参，只要把参数输进去，就能给出最优化的结果和参数。
# 但是这个方法适合于小数据集，一旦数据的量级上去了，很难得出结果。
# 数据量比较大的时候可以使用一个快速调优的方法——坐标下降。
# 它其实是一种贪心算法：拿当前对模型影响最大的参数调优，直到最优化；
# 再拿下一个影响最大的参数调优，如此下去，直到所有的参数调整完毕。这个方法的缺点就是可能会调到局部最优而不是全局最优
parameters = {'svc__C': [1, 5, 10, 50]}
grid = GridSearchCV(model, param_grid=parameters, cv=3)

grid.fit(x_train, y_train)
# print(grid.best_params_)
model = grid.best_estimator_
y_train_pred = model.predict(x_test)
print('支持向量机模型的平均准确度为: %s' % model.score(x_test, y_test))

# y_train_pred = svc.predict(x_test)
print('The predction result:', y_train_pred)
y_pred = pd.Series(y_train_pred)
# y_pred.to_csv("支持向量积.csv")
