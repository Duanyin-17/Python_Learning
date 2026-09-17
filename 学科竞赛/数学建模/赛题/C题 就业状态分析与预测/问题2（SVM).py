import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

# 读取数据
filename = '就失业状态分析结果1.xlsx'
data = pd.read_excel(filename)

# 定义特征变量
numeric_features = ['年龄']
categorical_features = ['婚姻状态', '教育程度', '政治面貌',  '文化程度']

# 将分类变量转换为数值型
for feature in categorical_features:
    data[feature] = data[feature].astype('category').cat.codes

# 创建特征矩阵 X 和目标变量 y
X_train = data[numeric_features + categorical_features].values
y_train = data['就业状态'].values

# 训练支持向量机
svm_mdl = SVC(kernel='linear', random_state=42)  # 使用线性核函数
svm_mdl.fit(X_train, y_train)

# 使用训练好的SVM模型进行预测
y_pred_train_svm = svm_mdl.predict(X_train)

# 计算评估指标
accuracy_svm = accuracy_score(y_train, y_pred_train_svm)
precision_svm = precision_score(y_train, y_pred_train_svm)
recall_svm = recall_score(y_train, y_pred_train_svm)
f1_score_svm = f1_score(y_train, y_pred_train_svm)

# 输出评估指标
metrics = pd.DataFrame({
    'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-score'],
    'SVM': [accuracy_svm, precision_svm, recall_svm, f1_score_svm]
})

# 输出模型评估结果表格
print("模型评估结果:")
print(metrics)

# 输出特征的重要性
feature_importance_svm = np.abs(svm_mdl.coef_.flatten())

features = numeric_features + categorical_features
feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importance_svm})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# 输出特征重要性排序
print("SVM Feature Importance Ranking:")
print(feature_importance_df)

# 预测新样本
predict_filename = '附件1 数据-C题.xls'
predict_data = pd.read_excel(predict_filename, sheet_name="预测集", skiprows=1)

# 数据预处理
for feature in categorical_features:
    predict_data[feature] = predict_data[feature].astype('category').cat.codes

# 创建特征矩阵 X
X_predict = predict_data[numeric_features + categorical_features].values

# 使用训练好的SVM模型进行预测
y_predict_svm = svm_mdl.predict(X_predict)

# 保存预测结果到文件
predict_data['PredictedEmploymentStatus'] = y_predict_svm
predict_data.to_excel('SVM_预测结果.xlsx', index=False)


#中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 可视化
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue')
plt.xlabel('Importance')
plt.title('SVM Feature Importance')
plt.grid(True)
plt.show()