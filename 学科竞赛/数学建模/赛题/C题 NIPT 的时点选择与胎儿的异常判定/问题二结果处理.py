import pandas as pd


df = pd.read_excel('问题二结果.xlsx')

# a = 0.04
#
# count_below_threshold = (df['Y染色体预测浓度'] < a).sum()
#
# print(f"Y预测浓度小于 {a} 的元素个数为：{count_below_threshold}")
#
# print(df1['孕妇BMI'].describe())

df1 = df[(df['孕妇BMI'] >= 26.618) & (df['孕妇BMI'] < 29.566)]
df2 = df[(df['孕妇BMI'] >= 29.566) & (df['孕妇BMI'] < 31.45)]
df3 = df[(df['孕妇BMI'] >= 31.45) & (df['孕妇BMI'] < 33.518)]
df4 = df[(df['孕妇BMI'] >= 33.518) & (df['孕妇BMI'] < 35.944)]
df5 = df[(df['孕妇BMI'] >= 35.944) & (df['孕妇BMI'] < 39.302)]

min_index = df1['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")

min_index = df2['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")

min_index = df3['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")

min_index = df4['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")

min_index = df5['风险'].idxmin()
min_row = df.loc[min_index]
print(f"整行数据：\n{min_row}")




