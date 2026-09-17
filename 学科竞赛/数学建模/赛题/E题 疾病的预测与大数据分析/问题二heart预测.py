import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 加载数据集
heart_df = pd.read_csv('heart_t.csv')

# 筛选出符合条件的特征
heart_features = ['Age', 'Sex', 'ChestPainType', 'Cholesterol', 'FastingBS', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']
heart_X = heart_df[heart_features]
heart_y = heart_df['HeartDisease']

# 划分训练集和测试集
heart_X_train, heart_X_test, heart_y_train, heart_y_test = train_test_split(heart_X, heart_y, test_size=0.2, random_state=42)

# 构建决策树模型
heart_model = DecisionTreeClassifier(random_state=42)
heart_model.fit(heart_X_train, heart_y_train)

# 预测
heart_y_pred = heart_model.predict(heart_X_test)

# 模型评估
heart_accuracy = accuracy_score(heart_y_test, heart_y_pred)
heart_report = classification_report(heart_y_test, heart_y_pred, zero_division=0)
heart_confusion = confusion_matrix(heart_y_test, heart_y_pred)

print("Heart Model Accuracy:", heart_accuracy)
print("Heart Model Classification Report:\n", heart_report)
print("Heart Model Confusion Matrix:\n", heart_confusion)