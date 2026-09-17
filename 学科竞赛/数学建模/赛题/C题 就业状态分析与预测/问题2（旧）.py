import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 读取数据
data = pd.read_excel(r"就失业状态分析结果.xlsx")

# 选择特征和目标变量
features = ['年龄', '婚姻状态', '教育程度', '政治面貌', '户籍地址', '宗教信仰', '文化程度']
target = '就业状态'

# 分离数值变量和分类变量
numerical_features = ['年龄']
categorical_features = ['婚姻状态', '教育程度', '政治面貌', '户籍地址', '宗教信仰', '文化程度']

# 分离数据
X = data[features]
y = data[target]

# 确保数值特征列的数据类型为浮点数
X.loc[:, numerical_features] = X[numerical_features].astype(float)

# 标准化数值变量
scaler = StandardScaler()
X.loc[:, numerical_features] = scaler.fit_transform(X[numerical_features])

# 独热编码分类变量
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_encoded = encoder.fit_transform(X[categorical_features])

# 合并特征
X = np.concatenate((X[numerical_features].values, X_encoded), axis=1)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 定义模型
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'SVM': SVC(kernel='linear', probability=True)
}

# 训练模型并评估
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results[name] = {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred, average='weighted'),  # 假设是多分类问题
        'Recall': recall_score(y_test, y_pred, average='weighted'),
        'F1-score': f1_score(y_test, y_pred, average='weighted')
    }
    print(f"{name} Results:")
    print(results[name])
    print("\n")