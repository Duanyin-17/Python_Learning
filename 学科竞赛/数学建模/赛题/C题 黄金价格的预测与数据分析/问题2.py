import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取数据
df = pd.read_csv('data_zh.csv')

# 2. 选择可能影响黄金价格的变量
variables = [
    '收盘价',  # 黄金价格
    '标普500收盘价', '道琼斯收盘价', '欧元兑美元汇率', '原油期货价格', '白银价格',
    '大豆期货价格', '美国国债价格', '美元指数', '黄金矿业ETF收盘', '原油ETF收盘'
]

# 3. 计算相关系数矩阵
correlation_matrix = df[variables].corr()

# 4. 绘制相关系数矩阵热力图
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5)
plt.title('变量之间的相关系数矩阵热力图')
plt.tight_layout()
plt.show()

# 5. 提取黄金价格与其他变量的相关系数
gold_correlation = correlation_matrix['收盘价'].sort_values(ascending=False)

print("\n黄金价格与其他变量的相关系数：")
print(gold_correlation)