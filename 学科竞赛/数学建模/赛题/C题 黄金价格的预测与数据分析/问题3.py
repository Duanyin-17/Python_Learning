import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取数据
df = pd.read_csv('data_zh.csv')

# 2. 选择特征变量和目标变量
features = ['黄金矿业ETF收盘','大豆期货价格','原油期货价格','原油ETF收盘','白银价格','美元指数','标普500收盘价']
target = '收盘价'

# 3. 划分训练集和测试集
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 建立线性回归模型
model = LinearRegression()
model.fit(X_train, y_train)

# 5. 在测试集上进行预测
y_pred = model.predict(X_test)

# 6. 评估模型效果
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"均方误差（MSE）: {mse:.2f}")
print(f"平均绝对误差（MAE）: {mae:.2f}")

# 7. 绘制实际值与预测值的对比图
plt.figure(figsize=(12, 6))
plt.plot(y_test.values, label='实际值', color='blue', linewidth=1.5)
plt.plot(y_pred, label='预测值', color='red', linewidth=1.5)
plt.title('黄金价格预测：实际值 vs 预测值')
plt.xlabel('样本索引')
plt.ylabel('黄金价格')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
