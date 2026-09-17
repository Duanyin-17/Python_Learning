import pandas as pd
import re

df = pd.read_excel("C:\\Users\\27047\\Desktop\\附件.xlsx",sheet_name='女胎检测数据')

print(f"数据量{df.shape[0]}")

print(df.isnull().sum())
df.dropna(inplace=True,subset = '末次月经')

df['孕妇BMI'] = df['孕妇BMI'].fillna(df['体重'] - df['身高']**2)

#周转化天数
def ctd(a):
    match = re.match(r'(\d+)w\+(\d+)',a)
    if match:
        weeks = int(match.group(1))
        days = int(match.group(2))
        return weeks * 7 + days
    match = re.match(r'(\d+)w',a)
    if match:
        weeks = int(match.group(1))
        return weeks * 7
    match = re.match(r'(\d+)W\+(\d+)', a)
    if match:
        weeks = int(match.group(1))
        days = int(match.group(2))
        return weeks * 7 + days
    return None

df['检测孕周'] = df['检测孕周'].apply(ctd)

#替换
replace = {
    'IVF妊娠':{'自然受孕':0,'IUI（人工授精）':1,'IVF（试管婴儿）':2},
    '怀孕次数':{1:1,2:2,'≥3':3},
    '胎儿是否健康':{'是':1,'否':0}
}
df = df.replace(replace)

# # GC删除不准确
# df = df[(df['GC含量'] >= 0.4) & (df['GC含量'] <= 0.6)]

# 删除Z值不准确
# df = df[(df['13号染色体的Z值'] >= -3) & (df['13号染色体的Z值'] <= 3)]
# df = df[(df['18号染色体的Z值'] >= -3) & (df['18号染色体的Z值'] <= 3)]
# df = df[(df['21号染色体的Z值'] >= -3) & (df['21号染色体的Z值'] <= 3)]
# df = df[(df['X染色体的Z值'] >= -3) & (df['X染色体的Z值'] <= 3)]

df['女胎异常'] = df['染色体的非整倍体'].notna().astype(int)

# df['染色体数目异常'] = ((df[['13号染色体的Z值','18号染色体的Z值','21号染色体的Z值']] < -2) | (df[['13号染色体的Z值','18号染色体的Z值','21号染色体的Z值']] > 2)).any(axis=1).astype(int)

col = ['年龄', '身高', '体重','IVF妊娠',
     '检测孕周', '孕妇BMI', '原始读段数', '在参考基因组上比对的比例',
     '重复读段的比例', '唯一比对的读段数', 'GC含量', '13号染色体的Z值', '18号染色体的Z值',
     '21号染色体的Z值', 'X染色体的Z值', 'X染色体浓度',
     '13号染色体的GC含量', '18号染色体的GC含量', '21号染色体的GC含量',
     '被过滤掉读段数的比例','怀孕次数', '生产次数', '胎儿是否健康','女胎异常']#,'染色体数目异常']

df[col] = df[col].astype(float)

df.to_excel('处理后数据(女胎).xlsx')
print("处理结果已保存")

print(f"数据量{df.shape[0]}")
