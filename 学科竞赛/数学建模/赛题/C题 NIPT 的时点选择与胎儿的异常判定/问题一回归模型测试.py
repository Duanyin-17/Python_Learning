import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import  Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

df = pd.read_excel('处理后数据.xlsx')

# df['孕妇BMI'] = df['孕妇BMI'].apply(lambda x: 1 if 20 <= x < 28 else 0)
# df['孕妇BMI'] = df['孕妇BMI'].apply(lambda x: 2 if 28 <= x < 32 else 0)
# df['孕妇BMI'] = df['孕妇BMI'].apply(lambda x: 3 if 32 <= x < 36 else 0)
# df['孕妇BMI'] = df['孕妇BMI'].apply(lambda x: 4 if 36 <= x < 40 else 0)
# df['孕妇BMI'] = df['孕妇BMI'].apply(lambda x: 5 if 40 <= x      else 0)


X = df[['检测孕周', '孕妇BMI']]
y = df['Y染色体浓度']

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

X_poly = np.hstack([X_poly, X['检测孕周'].values.reshape(-1, 1) + X['孕妇BMI'].values.reshape(-1, 1)])



ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_poly, y)
y_pred_ridge = ridge_model.predict(X_poly)
mse_ridge = mean_squared_error(y, y_pred_ridge)
r2_ridge = r2_score(y, y_pred_ridge)
print("岭回归 MSE：", mse_ridge)
print("岭回归 R²：", r2_ridge)

lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_poly, y)
y_pred_lasso = lasso_model.predict(X_poly)
mse_lasso = mean_squared_error(y, y_pred_lasso)
r2_lasso = r2_score(y, y_pred_lasso)
print("Lasso回归 MSE：", mse_lasso)
print("Lasso回归 R²：", r2_lasso)

tree_model = DecisionTreeRegressor(max_depth=3, random_state=42)
tree_model.fit(X_poly, y)
y_pred_tree = tree_model.predict(X_poly)
mse_tree = mean_squared_error(y, y_pred_tree)
r2_tree = r2_score(y, y_pred_tree)
print("决策树回归 MSE：", mse_tree)
print("决策树回归 R²：", r2_tree)

forest_model = RandomForestRegressor(n_estimators=100, random_state=42)
forest_model.fit(X_poly, y)
y_pred_forest = forest_model.predict(X_poly)
mse_forest = mean_squared_error(y, y_pred_forest)
r2_forest = r2_score(y, y_pred_forest)
print("随机森林回归 MSE：", mse_forest)
print("随机森林回归 R²：", r2_forest)

svr_model = SVR(kernel='rbf', C=1.0, epsilon=0.1)
svr_model.fit(X_poly, y)
y_pred_svr = svr_model.predict(X_poly)
mse_svr = mean_squared_error(y, y_pred_svr)
r2_svr = r2_score(y, y_pred_svr)
print("支持向量机回归 MSE：", mse_svr)
print("支持向量机回归 R²：", r2_svr)

r2_values = [r2_ridge, r2_lasso, r2_tree, r2_forest, r2_svr]

mse_values = [mse_ridge, mse_lasso, mse_tree, mse_forest, mse_svr]

models = ['岭回归', 'Lasso回归', '决策树回归', '随机森林回归', '支持向量机回归']

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 6))
plt.bar(models, r2_values, color='blue')
plt.xlabel('模型')
plt.ylabel('R^2')
plt.title('R^2')
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(models, mse_values, color='blue')
plt.xlabel('模型')
plt.ylabel('MSE')
plt.title('MSE')
plt.show()
