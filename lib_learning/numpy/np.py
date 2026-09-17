import numpy as np


#技巧
'''
# a = np.random.randn(5,1)
# 创建数组的时候不要用[5,]这种结构，说是容易出bug
# a = np.random.randn(5)

# a.reshape(5,1)

# assert(a.shape == (5,1)),"这里是断言的报错，前面为真才会运行"
# #随意插入assert来检验数组结构是否符合期望
# #不要害怕调用reshape来确保是你需要的维度
# print(a)
# print(a.shape)

'''

# ndarray类型创建
# np,array(object,dtype,ndmin)
#          数据    类型   最小维数

# np.arange(起始值,终值,步长)  不含终值
# np.arange(10)  创建0~9的数组

# np.linspace(起始值,终值,元素个数)  用于参数为浮点型
# np.logspace(a,b,元素个数)  创建从10^a到10^b的等比数列
# np.zeros(a)  创建全零数组，单个数值是一维，列表代表多维形状
# np.ones(a)  创建全1数组
# np.diag(a)  创建对角矩阵，对角线为指定值或零
# np.eyes(a)  创建对角线为1，其余为零的矩阵，边长为a

# ndarray 属性 ndim  shape  size   dtype   itemsize
#             秩     形状   元素个数 数据类型  每个元素字节大小

# ndarray 方法
# arr.astype(数据类型)  更改数据类型
# 例：arr2 = arr1.astype(np.float64)
# arr.shape = 形状   重新定义形状
# arr.reshape(形状)  副本  其中一个参数设为-1，可以由数据本身推断
# arr.ravel()       数据扁平化 展开为一维
# arr.flatten()     副本  两者参数相同order='C'按行优先‘F'按列优先
# 转置
# arr.T
# arr.transpose(轴顺序元组)  从0开始 像(0,1,2) -> (1,0,2)  转置后内存不连续，可能影响性能
# arr.swapaxes(轴1,轴2)    轴对换

# np 方法
# np.random
#   np.random,randint(最小值,最大值,size=数组形状) 区间内生成整数随机数组
#   np.random.rand() 生成0~1间的随机数组 多个元素代表多维
#   np.random.seed          确定随机数生成器种子
#             permutation   返回一个序列的随机排列或返回一个随机排列的范围
#             shuffle       对一个序列进行随机排序
#             binomial      产生二项分布的随机数
#             normal        产生正态（高斯）分布的随机数
#             beta          产生beta分布的随机数
#             chisquare     产生卡方分布的随机数
#             gamma         产生gamma分布的的随机数
#             uniform       产生在0~1间均匀分布的随机数
# 数组合并
# np,hstack(待合并数组组成的元组)   横向合并数组
# np.vstake                     纵向
# np.concatenate(元组,axis=0或1) 0横向1纵向
# 数组分割
# np.hsplit(arr,分割个数)
# np.vsplit(arr,分割个数)
# np.split(arr,分割个数，axis)    1横向0纵向
#
# np.where(condition,x,y) 满足条件输出x，不满足输出y，若只有条件输出满足条件元素的坐标
#

# 索引
# arr[索引] 切片类似python
# 多维数组索引用逗号分隔
# 例:arr[1,:2]
# arr[np.array([1,0,1],dtype = np.bool),1]  bool值索引

# 运算
# ufunc
# 基础运算 + - * / **
# 比较运算 >,<,==,>=,<=,!=  返回布尔数组
# 逻辑运算 np.any 逻辑or  np.all 逻辑and 运算结果范围布尔值
# 广播机制 所有输入向shape最长看齐

# 文件读写
# np.load('文件名.npy')      从二进制中读取数据
# np.save('文件名.npy',arr)  逸二进制格式保存数据
# np.loadtxt("arr.txt",delimiter = ",")     读文本文件，把文件加载到二维数组中
# np.savetxt("arr.txt",arr,fmt = "%d",delimiter = ",") 写
# np.genfromtxt("arr.txt",delimiter = ",")  结构化数组和缺失数据

# 数据统计与分析
# 排序
# np.sort(arr,axis,kind,order) 排序 axis=1沿横轴，0纵轴，None平坦化后排序，kind排序算法，order排序默认字段
# arr.argsort()  返回排序后的索引数组
# np.lexsort((arr1,arr2))   按arr1同时排序，返回每个元素的元素
# 去重
# np.unique(arr)  去重
# np.unique(arr,return_counts=True) 统计数组中每个元素出现的次数,并返回一个包含元素和对应出现次数的元组
# 重复
# np.tile(arr,reps) reps重复次数
# np.repeat(arr,reps,axis = None) axis沿指定抽重复0行1列
#
# np.sum(arr,axis = 0) 求和 axis0列1行 空求和所有
# np.mean(arr,axis = 0) 均值
# np.std(arr，axis = 0) 标准差
#



































