import pandas as pd
import numpy as np

# series

# obj = pd.Series([1,2,3,4,5]) # 注意大写
# print(obj)

# t = pd.Series([1,2,3,4,5],index = ['a','b','c','d','e'],name = 't')
# print(t)  # ↑指定索引
# print(t.index)
# # Index(['a', 'b', 'c', 'd', 'e'], dtype='object')
# # pandas底层基于numpy，np无可变长字符串类型 索引这个object代表指向python对象的引用
# print(t['a'])

# # 通过字典创建
# d = {'1':12,'2':13,'3':14,'4':15}
# # sdata = pd.Series(d)
# sdata = pd.Series(d,index = ["1","2","5"]) # 这样只会保留指定索引
# print(sdata)

# # 修改索引
# obj = pd.Series([1,2,3,4,5])
# obj.index = ['a','b','c','d','e']
# print(obj)


# DataFrame

# DataFrame创建
data = {
    'name':['张三','李四'],
    'age':[20,30],
    'sex':['male','female'],
    'city':['北京','上海']
}
# df = pd.DataFrame(data)
df = pd.DataFrame(data,columns=['name','age','sex','city'],index=['a','b']) # 这里也是部分筛选列名
print(df)                                     # index多余不会填充

# print(df.index)
# print(df.columns) # 打印列名
# print(df.values)
# print('条件判断:','name' in df.columns)
# print('表元素个数',df.size)
# print('表维度',df.ndim)
# print('表形状',df.shape)

# # 重建索引
# df.reindex(index = ['0','1'],columns = [1,2,3,4])
# print(df)
# print(df.reindex(columns = [1,2,3,4])) # 没有inplace属性
# # 会冲掉数据呢

# # 更换索引
# df.set_index('name',inplace=True)
# print(df,'\n')

# 数据查询
# print(df[['sex','age']])
# print(df['city'].head(2)) # head 前n行
# print(df['city'].tail(2)) # tail 后n行 默认值都是5
# print(df['city'].sample(2)) #随机抽取n行
# print(df['city'].sample(frac=0.5)) # 50%

# print(df.loc[['张三'],['city']])
# print(df.loc[:,['age','city']])
# print(df.loc[df['age']>25])
# print(df['city'].isin(['北京']))

# print(df.iloc[:3])
# print(df.iloc[[1],[1,2]])

# print(df.query('age>25 & age<31')['age'])
# print(df.age >=30)

# 数据修改
data1 = {'name':'小红','city':'武汉','age':27,'sex':'male'}
df = df.append(data1,ignore_index=True)
print(df,'\n')  # 会重新生成索引

# # df['year'] = [2001,2002,2003]
# # print(df,'\n')
# df.insert(0,'year',[2001,2002,2003])
# print(df,'\n')
#
# df.drop('year',axis=1,inplace=True)
# print(df,'\n')
# df.drop(df[df['city']=='武汉'].index,inplace=True)
# print(df,'\n')
#
# df.rename(columns={'name':'姓名'},inplace=True)
# print(df,'\n')

# 运算
# Series相加非对应元素用NaN代替
# DataFrame相加一样

# # 函数应用
# df['age'] = df['age'].map(lambda x:x+1)
# print(df)  # map仅套用在Series上
#
# print(df['age'].apply(np.mean))
#
# # df.applymap()  #作用在整个df

# # 排序
# df.sort_index()
# print(df)
# df.sort_values(by='age',ascending=False) # ascending=False 降序
# print(df)

# # 统计
# print(df['age'].sum())  # 求和 axis = 1 可以按行
# print(df.describe()) # 描述每个元素发分布状态
# print(df.sex.unique()) # 打印唯一值
# print(df.sex.nunique()) # 打印唯一值个数
# print(df.sex.value_counts()) # 打印该列各种取值

# 分组
# print(df.groupby('sex').size())
# 分组后的函数操作：
# .mean()   # 均值
# .count()  # 计数
# .median() # 中位数
# .sum()    # 求和
# .min()    # 最小
# .max()    # 最大
# .std()    # 标准差
# .var()    # 方差

# print(df.groupby([0,1,0]).size()) # 可以直接输入个列表进行分组

# 数据聚合
print(df.agg({'age':np.mean,'name':max,'city':max}))
print(df.groupby(['sex'],as_index=False).agg({'age':np.mean,'name':max,'city':max}))
#                            as_index=False 可以让分组的键不作为结果的索引 默认True






