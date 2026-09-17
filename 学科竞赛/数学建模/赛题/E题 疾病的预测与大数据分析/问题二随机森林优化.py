import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 加载数据集
cirrhosis_df = pd.read_csv('cirrhosis_t.csv')

# 筛选出符合条件的特征
cirrhosis_features = ['N_Days', 'Status', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema', 'Bilirubin', 'Copper', 'Platelets', 'Prothrombin']
cirrhosis_X = cirrhosis_df[cirrhosis_features]
cirrhosis_y = cirrhosis_df['Stage']

# 划分训练集和测试集
cirrhosis_X_train, cirrhosis_X_test, cirrhosis_y_train, cirrhosis_y_test = train_test_split(cirrhosis_X, cirrhosis_y, test_size=0.2, random_state=42)

# 构建随机森林模型
cirrhosis_model = RandomForestClassifier(random_state=42)

# 训练模型
cirrhosis_model.fit(cirrhosis_X_train, cirrhosis_y_train)

# 预测
cirrhosis_y_pred = cirrhosis_model.predict(cirrhosis_X_test)

# 模型评估
cirrhosis_accuracy = accuracy_score(cirrhosis_y_test, cirrhosis_y_pred)
cirrhosis_report = classification_report(cirrhosis_y_test, cirrhosis_y_pred, zero_division=0)
cirrhosis_confusion = confusion_matrix(cirrhosis_y_test, cirrhosis_y_pred)

print("Cirrhosis Model Accuracy:", cirrhosis_accuracy)
print("Cirrhosis Model Classification Report:\n", cirrhosis_report)
print("Cirrhosis Model Confusion Matrix:\n", cirrhosis_confusion)