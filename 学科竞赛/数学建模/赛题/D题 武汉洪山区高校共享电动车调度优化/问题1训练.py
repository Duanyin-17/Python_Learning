import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

file_path = "C:\\Users\\27047\\Desktop\\数据.xlsx"
df = pd.read_excel(file_path, sheet_name='历史用车数据',usecols=['日期','时间段','区域编号','是否降雨','是否工作日','实际需求数量（台）'], engine='openpyxl')

# 数据预处理
# 将日期转换为星期几（周一为0，周日为6）
df['日期'] = pd.to_datetime(df['日期'])

# 将时间段转换为数值（早为0，中为1，晚为2）
time_mapping = {'07:00–09:00': 0, '12:00–14:00': 1, '17:00–19:00': 2}
df['时间段'] = df['时间段'].map(time_mapping)

# 将区域编号转换为数值
df['区域编号'] = df['区域编号'].astype('category').cat.codes

# 特征和目标变量
X = df[['日期', '时间段', '区域编号', '是否降雨', '是否工作日']]
y = df['实际需求数量（台）']

# 将日期转换为时间戳
X['日期'] = X['日期'].apply(lambda x: int(x.timestamp()))

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练随机森林模型
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)

# 预测
y_pred = rf.predict(X_test)

# 评估模型
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# 保存模型
import joblib
joblib.dump(rf, 'random_forest_model.pkl')