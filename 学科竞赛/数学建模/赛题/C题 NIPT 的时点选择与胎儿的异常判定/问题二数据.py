import pandas as pd

#  生成问题二预测数据

df = pd.read_excel('处理后数据.xlsx')
df = df.sort_values(by='孕妇BMI')

# # 倍化
# x1 = 77
# x2 = 100
# repeated_data = df['孕妇BMI'].repeat(x2-x1).reset_index(drop=True)
# repeated_data1 = df['差值'].repeat(x2-x1).reset_index(drop=True)
# tt = np.tile(np.arange(x1,x2), len(df))
# new_df = pd.DataFrame({'孕妇BMI': repeated_data, '时点': tt,'差值':repeated_data1})
#
# new_df.to_excel('问题二预测数据.xlsx',index=False)

# df['检测孕周'] = df['检测孕周']/7
# print(new_df['时点'].describe())

df_c = df[['孕妇BMI','检测孕周','Y染色体浓度']]
df_c = df_c.rename(columns={'检测孕周': '时点'})
df_c.to_excel('问题二预测数据.xlsx',index=False)




