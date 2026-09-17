import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

df = pd.read_excel('处理后数据.xlsx')

X = df[['身高','体重', '年龄','孕妇BMI']]
y = df['Y染色体浓度']

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

rf_model = RandomForestRegressor(n_estimators=100, oob_score=True, random_state=42)
rf_model.fit(X_poly, y)

y_pred_rf = rf_model.predict(X_poly)

r2_rf = r2_score(y, y_pred_rf)
mse_rf = mean_squared_error(y, y_pred_rf)
print("随机森林回归 R^2：", r2_rf)
print("随机森林回归 MSE：", mse_rf)

joblib.dump(rf_model, '保存的模型文件2.pkl')
print("模型已保存")