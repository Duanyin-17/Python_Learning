import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
import joblib

rf_model = joblib.load('保存的模型文件1.pkl')
df = pd.read_excel('问题二预测数据.xlsx')

X_new = df[['时点', '孕妇BMI']]

poly = PolynomialFeatures(degree=2, include_bias=False)
X_new_poly = poly.fit_transform(X_new)

X_new_poly = np.hstack([X_new_poly, X_new['时点'].values.reshape(-1, 1) + X_new['孕妇BMI'].values.reshape(-1, 1)])

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

df.to_excel('问题二结果.xlsx',index = False)
print('结果已保存')








