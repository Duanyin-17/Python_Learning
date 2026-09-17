import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_excel('处理后数据.xlsx')

df['检测孕周'] = df['检测孕周']/7



col = ['年龄', '身高', '体重','IVF妊娠',
     '检测孕周', '孕妇BMI', '原始读段数', '在参考基因组上比对的比例',
     '重复读段的比例', '唯一比对的读段数  ', 'GC含量', '13号染色体的Z值', '18号染色体的Z值',
     '21号染色体的Z值', 'X染色体的Z值', 'Y染色体的Z值', 'Y染色体浓度', 'X染色体浓度',
     '13号染色体的GC含量', '18号染色体的GC含量', '21号染色体的GC含量',
     '被过滤掉读段数的比例','怀孕次数', '生产次数', '胎儿是否健康']



df = df.drop_duplicates(subset=['孕妇BMI'])

corr_matrix = df[col].corr(method='spearman')

# print(corr_matrix)

df_corr_matrix = pd.DataFrame(corr_matrix,index = ['年龄', '身高', '体重','IVF妊娠',
     '检测孕周', '孕妇BMI', '原始读段数', '在参考基因组上比对的比例',
     '重复读段的比例', '唯一比对的读段数  ', 'GC含量', '13号染色体的Z值', '18号染色体的Z值',
     '21号染色体的Z值', 'X染色体的Z值', 'Y染色体的Z值', 'X染色体浓度',
     '13号染色体的GC含量', '18号染色体的GC含量', '21号染色体的GC含量',
     '被过滤掉读段数的比例','怀孕次数', '生产次数', '胎儿是否健康'])
t = 'Y染色体浓度'
correlations = df_corr_matrix[t]
plt.figure(figsize=(10, 6))
correlations.plot(kind='barh', color='skyblue')
plt.show()

corr_yconcentration = corr_matrix[t].drop(t)

print("\nY：",end='')
print(corr_yconcentration)
