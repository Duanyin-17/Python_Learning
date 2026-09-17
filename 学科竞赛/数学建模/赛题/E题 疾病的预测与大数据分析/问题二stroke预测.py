import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 加载数据集
stroke_df = pd.read_csv('stroke_t.csv')

# 筛选出符合条件的特征
stroke_features = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level']
stroke_X = stroke_df[stroke_features]
stroke_y = stroke_df['stroke']

# 划分训练集和测试集
stroke_X_train, stroke_X_test, stroke_y_train, stroke_y_test = train_test_split(stroke_X, stroke_y, test_size=0.2, random_state=42)

# 构建决策树模型
stroke_model = DecisionTreeClassifier(random_state=42)
stroke_model.fit(stroke_X_train, stroke_y_train)

# 预测
stroke_y_pred = stroke_model.predict(stroke_X_test)

# 模型评估
stroke_accuracy = accuracy_score(stroke_y_test, stroke_y_pred)
stroke_report = classification_report(stroke_y_test, stroke_y_pred, zero_division=0)
stroke_confusion = confusion_matrix(stroke_y_test, stroke_y_pred)

print("Stroke Model Accuracy:", stroke_accuracy)
print("Stroke Model Classification Report:\n", stroke_report)
print("Stroke Model Confusion Matrix:\n", stroke_confusion)