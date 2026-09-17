import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 加载数据集
cirrhosis_df = pd.read_csv('cirrhosis_t.csv')

# 筛选出符合条件的特征
cirrhosis_features = ['N_Days', 'Status', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema', 'Bilirubin', 'Copper', 'Platelets', 'Prothrombin']
cirrhosis_X = cirrhosis_df[cirrhosis_features]
cirrhosis_y = cirrhosis_df['Stage']

# 划分训练集和测试集
cirrhosis_X_train, cirrhosis_X_test, cirrhosis_y_train, cirrhosis_y_test = train_test_split(cirrhosis_X, cirrhosis_y, test_size=0.2, random_state=42)

# 构建决策树模型
cirrhosis_model = DecisionTreeClassifier(random_state=42)

# 定义参数网格
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']  # 移除 'auto' 选项
}

# 初始化网格搜索
grid_search = GridSearchCV(estimator=cirrhosis_model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

# 在训练数据上执行网格搜索
grid_search.fit(cirrhosis_X_train, cirrhosis_y_train)

# 输出最佳参数和最佳分数
print("Best parameters:", grid_search.best_params_)
print("Best cross-validation score: {:.2f}".format(grid_search.best_score_))

# 使用最佳参数的模型
best_model = grid_search.best_estimator_

# 预测
cirrhosis_y_pred = best_model.predict(cirrhosis_X_test)

# 模型评估
cirrhosis_accuracy = accuracy_score(cirrhosis_y_test, cirrhosis_y_pred)
cirrhosis_report = classification_report(cirrhosis_y_test, cirrhosis_y_pred, zero_division=0)
cirrhosis_confusion = confusion_matrix(cirrhosis_y_test, cirrhosis_y_pred)

print("Cirrhosis Model Accuracy:", cirrhosis_accuracy)
print("Cirrhosis Model Classification Report:\n", cirrhosis_report)
print("Cirrhosis Model Confusion Matrix:\n", cirrhosis_confusion)