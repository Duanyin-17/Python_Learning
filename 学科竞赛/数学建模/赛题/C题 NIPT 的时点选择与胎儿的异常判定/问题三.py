import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
import joblib




rf_model = joblib.load('保存的模型文件2.pkl')
df = pd.read_excel('问题三预测数据.xlsx')

X_new = df[['身高','体重', '年龄','孕妇BMI']]

poly = PolynomialFeatures(degree=2, include_bias=False)
X_new_poly = poly.fit_transform(X_new)


y_pred_new = rf_model.predict(X_new_poly)

df['Y染色体预测浓度'] = y_pred_new

a = 0.04

count_below_threshold = (df['Y染色体预测浓度'] < a).sum()

print(f"小于 {a} 的元素个数为：{count_below_threshold}")

s1 = 50
s2 = 50
h1 = h2 = h3 = 1

def fun2(x):
    #return abs(0.04 - x) * (1)
    return 0 if x >= 0.04 else s1*(0.04-x)#*(-1)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))



# .apply(lambda x: sigmoid(x))
df['风险'] = (1)*(h1)*(np.tanh(  (df['时点']-77)))  +  h2*(df['Y染色体预测浓度'].apply(lambda x: fun2(x)))  +  h3*s2*abs(df['Y染色体预测浓度']-df['Y染色体浓度'])

df1 = df[(df['孕妇BMI'] >= 26.618) & (df['孕妇BMI'] < 29.566)]
df2 = df[(df['孕妇BMI'] >= 29.566) & (df['孕妇BMI'] < 31.45)]
df3 = df[(df['孕妇BMI'] >= 31.45) & (df['孕妇BMI'] < 33.518)]
df4 = df[(df['孕妇BMI'] >= 33.518) & (df['孕妇BMI'] < 35.944)]
df5 = df[(df['孕妇BMI'] >= 35.944) & (df['孕妇BMI'] < 39.302)]

a = ((df1['Y染色体浓度'] > 0.04).sum())/df1.shape[0]
print(f"{a*100:.2f}%")
df1 = df1.iloc[df['风险']] - a
a = ((df2['Y染色体浓度'] > 0.04).sum())/df2.shape[0]
print(f"{a*100:.2f}%")
df2 = df2.iloc[df['风险']] - a
a = ((df3['Y染色体浓度'] > 0.04).sum())/df3.shape[0]
print(f"{a*100:.2f}%")
df3 = df3.iloc[df['风险']] - a
a = ((df4['Y染色体浓度'] > 0.04).sum())/df4.shape[0]
print(f"{a*100:.2f}%")
df4 = df4.iloc[df['风险']] - a
a = ((df5['Y染色体浓度'] > 0.04).sum())/df5.shape[0]
print(f"{a*100:.2f}%")
df5 = df5.iloc[df['风险']] - a


min_index = df1['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")

min_index = df2['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")

min_index = df3['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")

min_index = df4['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")

min_index = df5['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")


df.to_excel('问题三结果.xlsx',index = False)
print('结果已保存')



