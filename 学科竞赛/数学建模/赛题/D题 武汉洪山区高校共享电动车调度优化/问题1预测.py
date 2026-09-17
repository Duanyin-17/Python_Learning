import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor

# 导入预测数据
file_path = "C:\\Users\\27047\\Desktop\\预测数据.xlsx"
future_df = pd.read_excel(file_path, usecols=['日期', '时间段', '区域编号', '是否降雨', '是否工作日'], engine='openpyxl')

# 数据预处理
future_df['日期'] = pd.to_datetime(future_df['日期'])

# 将时间段转换为数值（早为0，中为1，晚为2）
time_mapping = {'07:00–09:00': 0, '12:00–14:00': 1, '17:00–19:00': 2}
future_df['时间段'] = future_df['时间段'].map(time_mapping)

# 将区域编号转换为数值
future_df['区域编号'] = future_df['区域编号'].astype('category').cat.codes



# 特征和目标变量
X_future = future_df[['日期','时间段', '区域编号', '是否降雨', '是否工作日']]

X_future['日期'] = X_future['日期'].apply(lambda x: int(x.timestamp()))

# 加载模型
model = joblib.load('random_forest_model.pkl')

# 预测
predictions = model.predict(X_future)



# 将预测结果添加到DataFrame中
future_df['预测需求数量（台）'] = predictions

future_df['预测需求数量（台）'] = np.around(predictions).astype(int)

# 输出预测结果
print(future_df[['日期', '时间段', '区域编号', '预测需求数量（台）']])

future_df.to_excel('C:\\Users\\27047\\Desktop\\预测结果.xlsx', index=False)