import pandas as pd


#  生成问题三预测数据
df = pd.read_excel('处理后数据.xlsx')
df = df.sort_values(by='孕妇BMI')


# df['检测孕周'] = df['检测孕周']/7
# print(new_df['时点'].describe())

df_c = df[['身高','体重', '年龄','检测孕周','孕妇BMI','Y染色体浓度']]
df_c = df_c.rename(columns={'检测孕周': '时点'})
df_c.to_excel('问题三预测数据.xlsx',index=False)




