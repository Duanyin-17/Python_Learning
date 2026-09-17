import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_excel('处理后数据.xlsx')

# df['检测孕周'] = df['检测孕周']/7

X = df[['检测孕周', '孕妇BMI']]
y = df['Y染色体浓度']

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

X_poly = np.hstack([X_poly, X['检测孕周'].values.reshape(-1, 1) + X['孕妇BMI'].values.reshape(-1, 1)])

rf_model = RandomForestRegressor(n_estimators=100,oob_score=True,random_state=42)
rf_model.fit(X_poly, y)

y_pred_rf = rf_model.predict(X_poly)

r2_rf = r2_score(y, y_pred_rf)
mse_rf = mean_squared_error(y, y_pred_rf)
print("随机森林回归 R^2：", r2_rf)
print("随机森林回归 MSE：", mse_rf)

joblib.dump(rf_model, '保存的模型文件1.pkl')
print("模型已保存")

