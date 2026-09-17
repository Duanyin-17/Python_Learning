import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from scipy.stats import chi2_contingency

# 读取数据
data = pd.read_excel(r"就失业状态分析结果1.xlsx")

# 填充数值变量的缺失值
numerical_columns = ['年龄']
data[numerical_columns] = data[numerical_columns].fillna(data[numerical_columns].median())

# 填充分类变量的缺失值
categorical_columns = [col for col in data.columns if col not in numerical_columns and col != '就业状态']
data[categorical_columns] = data[categorical_columns].fillna(data[categorical_columns].mode().iloc[0])

# 对分类变量进行编码
label_encoder = LabelEncoder()
for column in categorical_columns:
    data[column] = label_encoder.fit_transform(data[column])

# 计算数值变量与就业状态的相关性
correlation_matrix = data.corr()
correlation_with_employment_status = correlation_matrix['就业状态']
print("数值变量与就业状态的相关性：")
print(correlation_with_employment_status[numerical_columns])

# 存储卡方检验的结果
chi2_results = []

# 计算分类变量与就业状态的卡方检验
for var in categorical_columns:
    if var != '就业状态':
        # 创建列联表
        contingency_table = pd.crosstab(data['就业状态'], data[var])
        # 进行卡方检验
        chi2_stat, pval, dof, expected = chi2_contingency(contingency_table)

        # 将结果存储到列表中
        chi2_results.append([var, '就业状态', chi2_stat, pval])

# 将结果转换为 DataFrame
chi2_results_df = pd.DataFrame(chi2_results, columns=['变量', '目标变量', '卡方统计量', 'P值'])

# 显示卡方检验的结果
print("\n分类变量与就业状态的卡方检验结果：")
print(chi2_results_df)

#中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 可视化
plt.figure(figsize=(12, 8))
sns.boxplot(x='就业状态', y='年龄', data=data)
plt.title('就业状态与年龄的箱线图')
plt.show()

plt.figure(figsize=(12, 8))
sns.heatmap(data[categorical_columns].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('分类变量之间的相关性热图')
plt.show()