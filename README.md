
乡村致贫数据分析

分析所给的表以及表中数据，在该案例中我们选取T_XCZXJ_JTCYXX表(家庭成员信息表)与T_XCZXJ_JTXX表(家庭信息表)来进行数据探索、数据处理以及模型建立步骤来建立正确的模型来判断一个家庭是否会致贫。选取了T_XCZXJ_YBSJXX表(医保数据信息)来根据医保自付金额来判断该人是否会返贫。接下来就是对上述三个表的处理过程。


***\*2.\**** ***\*数据探索\****

数据探索是拿到数据要做的第一步，目的是对要分析的数据有个大概的了解。弄清数集质量，大小，特征和样本数量，数据类型，数据的概率分布等。数据探索主要包括：数据质量探索、数据特征分析。

数据质量探索顾名思义，就是了解数据的大体质量，常见的数据问题比如缺失，异常值与数据不一致。数据特征分析包括分布情况（可以绘制频率分布直方图hist***\*，\****条形图***\*，\****饼图pie）。

对比分析：了解相互联系的指标的变化情况对比，考虑使用折线图plot。统计量分析：集中趋势分析：平均数data.mean()，中位数data.median()，众数。离散程度分析：极差，标准差data.std()，变异系数。变异系数=（标准差 / 平均数）×100%***\*，\****用来比较不同单位的数据的离散程度，而标准差一般用于比较相同单位。相关性分析：一般来说可以通过绘制散点图，来分析2个变量间的相关性。

 

2.1 属性探索


2.1.1、家庭信息表字段：


***\*3.\*******\*数据处理\****

数据预处理（data preprocessing）是指在主要的处理以前对数据进行的一些处理。数据的质量，直接决定了模型的预测和泛化能力的好坏。它涉及很多因素，包括：准确性、完整性、一致性、时效性、可信性和解释性。而在真实数据中，我们拿到的数据可能包含了大量的缺失值，可能包含大量的噪音，也可能因为人工录入错误导致有异常点存在，非常不利于算法模型的训练。数据清洗的结果是对各种脏数据进行对应方式的处理，得到标准的、干净的、连续的数据，提供给数据统计、数据挖掘等使用。

 

3.1 数据归约

数据归约技术可以用来得到数据集的归约表示，它小得多，但仍接近地保持原数据的完整性。 这样，在归约后的数据集上挖掘将更有效，并产生相同(或几乎相同)的分析结果。一般有如下策略：

1、维度规约

用于数据分析的数据可能包含数以百计的属性，其中大部分属性与挖掘任务不相关，是冗余的。维度归约通过删除不相关的属性，来减少数据量，并保证信息的损失最小。


· 逐步向前选择：该过程由空属性集开始，选择原属性集中最好的属性，并将它添加到该集合
中。在其后的每一次迭代，将原属性集剩下的属性中的最好的属性添加到该集合中。 

· 逐步向后删除：该过程由整个属性集开始。在每一步，删除掉尚在属性集中的最坏属性。

· 向前选择和向后删除的结合：向前选择和向后删除方法可以结合在一起，每一步选择一个最 好的属性，并在剩余属性中删除一个最坏的属性。

python scikit-learn 中的递归特征消除算法Recursive feature elimination (RFE)，就是利用这样的思想进行特征子集筛选的，一般考虑建立SVM或回归模型。

***\*单变量重要性：\****分析单变量和目标变量的相关性，删除预测能力较低的变量。这种方法不同于属性子集选择，通常从统计学和信息的角度去分析。

· pearson相关系数和卡方检验，分析目标变量和单变量的相关性。

· 回归系数：训练线性回归或逻辑回归，提取每个变量的表决系数，进行重要性排序。

· 树模型的Gini指数：训练决策树模型，提取每个变量的重要度，即Gini指数进行排序。

· Lasso正则化：训练回归模型时，加入L1正则化参数，将特征向量稀疏化。

· IV指标：风控模型中，通常求解每个变量的IV值，来定义变量的重要度，一般将阀值设定在0.02以上。

通常的做法是根据业务需求来定，如果基于业务的用户或商品特征，需要较多的解释性，考虑采用统计上的一些方法，如变量的分布曲线，直方图等，再计算相关性指标，最后去考虑一些模型方法。如果建模需要，则通常采用模型方法去筛选特征，如果用一些更为复杂的GBDT，DNN等模型，一般不做特征选择，而做特征交叉。

2、维度变换：

维度变换是将现有数据降低到更小的维度，尽量保证数据信息的完整性。楼主将介绍常用的几种有损失的维度变换方法，将大大地提高实践中建模的效率

· 主成分分析（PCA）和因子分析（FA）：PCA通过空间映射的方式，将当前维度映射到更低的维度，使得每个变量在新空间的方差最大。FA则是找到当前特征向量的公因子（维度更小），用公因子的线性组合来描述当前的特征向量。

· 奇异值分解（SVD）：SVD的降维可解释性较低，且计算量比PCA大，一般用在稀疏矩阵上降维，例如图片压缩，推荐系统。

· 聚类：将某一类具有相似性的特征聚到单个变量，从而大大降低维度。

· 线性组合：将多个变量做线性回归，根据每个变量的表决系数，赋予变量权重，可将该类变量根据权重组合成一个变量。

· 流行学习：流行学习中一些复杂的非线性方法，

 

3.2 数据变换和清洗

数据变换包括对数据进行规范化，离散化，稀疏化处理，达到适用于挖掘的目的。

\***\*2、离散化处理：\****数据离散化是指将连续的数据进行分段，使其变为一段段离散化的区间。分段的原则有基于等距离、等频率或优化的方法。数据离散化的原因主要有以下几点：

· 模型需要：比如决策树、朴素贝叶斯等算法，都是基于离散型的数据展开的。如果要使用该类算法，必须将离散型的数据进行。有效的离散化能减小算法的时间和空间开销，提高系统对样本的分类聚类能力和抗噪声能力。

· 离散化的特征相对于连续型特征更易理解。

· 可以有效的克服数据中隐藏的缺陷，使模型结果更加稳定。

等频法：使得每个箱中的样本数量相等，例如总样本n=100，分成k=5个箱，则分箱原则是保证落入每个箱的样本量=20。

等宽法：使得属性的箱宽度相等，例如年龄变量（0-100之间），可分成 [0,20]，[20,40]，[40,60]，[60,80]，[80,100]五个等宽的箱。

聚类法：根据聚类出来的簇，每个簇中的数据为一个箱，簇的数量模型给定。

***\*3、稀疏化处理：\****针对离散型且标称变量，无法进行有序的LabelEncoder时，通常考虑将变量做0，1哑变量的稀疏化处理，例如动物类型变量中含有猫，狗，猪，羊四个不同值，将该变量转换成is_猪，is_猫，is_狗，is_羊四个哑变量。若是变量的不同值较多，则根据频数，将出现次数较少的值统一归为一类'rare'。稀疏化处理既有利于模型快速收敛，又能提升模型的抗噪能力。

我们这里主要对一些离散属性，比如残疾等级、残疾类别等离散离散数据进行数据变换，修改该属性列的值。

 

3.2.1 修改某些属性列的值 


 

3.2.2 处理表中的空值

若缺失率较低（小于95%）且重要性较低，则根据数据分布的情况进行填充。对于数据符合均匀分布，用该变量的均值填补缺失，对于数据存在倾斜分布的情况，采用中位数进行填补。

· 插值法填充：包括随机插值，多重差补法，热平台插补，拉格朗日插值，牛顿插值等

· 模型填充：使用回归、贝叶斯、随机森林、决策树等模型对缺失数据进行预测。

**·** ***\*哑变量填充\****：若变量是离散型，且不同值较少，可转换成哑变量，例如性别SEX变量，存在male,fameal,NA三个不同的值，可将该列转换成 IS_SEX_MALE, IS_SEX_**FEMALE, IS_SEX_NA。若某个变量存在十几个不同的值，可根据每个值的频数，将频数较小的值归为一类'other'，降低维度。**此做法可最大化保留变量的信息。


 

3.2.3 数据集成

数据分析任务多半涉及数据集成。数据集成将多个数据源中的数据结合成、存放在一个一致的数据存储，如数据仓库中。这些源可能包括多个数据库、数据方或一般文件。 

\1. 实体识别问题：例如，数据分析者或计算机如何才能确信一个数 据库中的 customer_id 和另一个数据库中的 cust_number 指的是同一实体?通常，数据库和数据仓库 有元数据——关于数据的数据。这种元数据可以帮助避免模式集成中的错误。

\2. 冗余问题。一个属性是冗余的，如果它能由另一个表“导出”;如年薪。属性或 维命名的不一致也可能导致数据集中的冗余。 用相关性检测冗余：数值型变量可计算相关系数矩阵，标称型变量可计算卡方检验。

\3. 数据值的冲突和处理：不同数据源，在统一合并时，保持规范化，去重。

 

观察上部分处理后的表中数据可以发现每个属性列都代表一定的含义，每个属性的值都通过数字来进行分级了，在ZXSZK（在校生状况）中数字越大表示学历越高，在JKZK（健康状况）中数字越小表示该家庭成员健康状况越好，在CJDJ（残疾等级）中数字越小表示残疾等级越低，CJLB（残疾类别）中数字越小表示残疾情况越不严重，在LDJN（劳动技能）中数字越小表示劳动技能越好，在SFSW（是否死亡）为0则为已死亡，为1则表示存活。


 

 

***\*4.\*******\*数据处理后的可视化及分析\****

数据可视化是利用计算机图形学和图像处理技术，将数据转换成图形或图像在屏幕上显示出来，并进行交互处理的理论、方法和技术。数据可视化的实质是借助图形化手段，清晰有效的传达与沟通信息，使通过数据表达的内容更容易被理解。

数据可视化的主要特点是：

· 交互性。用户可以方便的以交互的方式管理和开发数据。

· 多维性。可以看到表示对象或事件的数据的多个属性或变量，而数据可以按其每一维的值，将其分类、排序、组合和显示。

· 可视性。数据可以用图像、曲线、二维图形、三维体和动画来显示，并可对其模式和相互关系进行可视化分析。


***\*5.\*******\*模型构建\****

模型构建是对采样数据轨迹的概括，它反映的是采样数据内部结构的一般特征，并与该采样数据的具体结构基本吻合。

预测模型的构建通常包括模型建立、模型训练、模型验证和模型预测4个步骤，但根据不同的数据挖掘分类应用会有细微的变化。

可以采取模型评价探究模型是否合适，以及不同模型之间的优劣。

模型效果评价通常分两步：

第一步，直接使用原来建立模型的样本数据来进行检验。

第二步，另找一批反映客观实际的、规律性的数据。

假如进行模型评价时第一步都通不过，那么所建立的决策支持信息价值就不太大了。

一般来说，模型评价在第一步应得到较好的反馈，从而说明我们确实从这批数据样本中挖掘出了符合实际的规律性。

在进行特征工程之后，我们一般会建立2-3个模型，来比较这几个模型在这个任务上哪个模型更好。例如：分类模型：KNN、贝叶斯分类、决策树、随机森林、SVM、逻辑回归。回归模型：简单线性回归、多重线性回归、一元非线性回归、lasso回归、岭回归。聚类模型：k-means、DBSCAN密度法、层次聚类法。一般这些模型可以直接使用sklearn中对应的模型。

 

5.1 构建Logistic逻辑回归模型

Logistic回归是一种十分常见的分类模型，是的严格来说这是一个分类模型，之所以叫做回归也是由于历史原因。不同于线性回归中对于参数的推导，我们在这里运用的方式不再是最小二乘法，而是极大似然估计。Logistic回归分析属于非线性回归，它是研究因变量为二项分类或多项分类结果与某些影响因素之间关系的一种多重回归分析方法。

 

 

1、Logistic回归建模步骤

①根据分析目的设置指标变量（因变量和自变量），然后收集数据，根据收集到的数据对特征再次进行筛选。

②y取1的概率是p=P(y=1|X)，取0的概率是1-p，用ln(p/(1-p))和自变量列出线性回归方程，估计出模型中的回归系数。

③进行模型检验。模型的有效性的检验指标有很多，最基本的有正确率，其次有混淆矩阵、ROC曲线、KS值等。

④模型应用：输入自变量的值，就可以得到预测变量的值。

 

2、参数调优：

***\*正则化参数\****：

***\*损失函数优化器\****：

 

3、模型预测结果：



5.2 构建SVM支持向量机模型

1、支持向量机建模步骤

①根据分析目的设置指标变量（因变量和自变量），然后收集数据，根据收集到的数据对特征再次进行筛选。

②使用PCA主成分分析，对特征进行筛选，这里选择的参数是6，即留下六个特征（虽然总共才七个特征）。使用make_pipeline1构建管道，实现流水化统一处理进行惩罚系数调优，加入模型进行从特征到模型的训练。

③用GridSearchCV对惩罚系数C进行自动调参，获得最优的参数和模型。这里得到的grid.best_estimator是50。

④进行模型检验。模型的有效性的检验指标有很多，最基本的有正确率，其次有混淆矩阵、ROC曲线、KS值等。

⑤模型应用：输入自变量的值，就可以得到预测变量的值。

 

2、参数调优：

***\*核函数：\****

· 线性核函数 LINEAR

· 高斯径向基核函数 RBF

· 多项式核函数 POLY

· 神经元的非线性作用核函数 Sigmoid

***\*惩罚系数\****：默认值为1.0， 错误项的惩罚系数。

 

 

3、模型预测结果：

对家庭各信息的数据情况进行支持向量机建模，通过4:1的比例将原数据集分为训练集以及测试集。再使用调优之后的模型对数据进行训练和测试，得到最优的惩罚系数是50，预测结果，可以把预测结果和家庭信息ID共同写入到“家庭致贫风险表2”。
