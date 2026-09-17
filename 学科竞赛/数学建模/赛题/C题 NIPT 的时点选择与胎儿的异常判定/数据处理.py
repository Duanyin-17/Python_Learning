import pandas as pd
import re

liuying = pd.read_excel("C:\\Users\\27047\\Desktop\\附件.xlsx",sheet_name='男胎检测数据')

a = 0.04

count_below_threshold = (liuying['Y染色体浓度'] < a).sum()

print(f"小于 {a} 的元素个数为：{count_below_threshold}")

#删缺失值
print(liuying.isnull().sum())
liuying.dropna(inplace=True,subset = '末次月经')


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

liuying['检测孕周'] = liuying['检测孕周'].apply(ctd)

#替换
replace = {
    'IVF妊娠':{'自然受孕':0,'IUI（人工授精）':1,'IVF（试管婴儿）':2},
    '怀孕次数':{1:1,2:2,'≥3':3},
    '胎儿是否健康':{'是':1,'否':0}
}
liuying = liuying.replace(replace)

#
# df.head(10)

#取可能相关的变量，转化浮点型
col = ['年龄', '身高', '体重','IVF妊娠',
    '检测孕周', '孕妇BMI', '原始读段数', '在参考基因组上比对的比例',
    '重复读段的比例', '唯一比对的读段数  ', 'GC含量', '13号染色体的Z值', '18号染色体的Z值',
    '21号染色体的Z值', 'X染色体的Z值', 'Y染色体的Z值', 'Y染色体浓度', 'X染色体浓度',
    '13号染色体的GC含量', '18号染色体的GC含量', '21号染色体的GC含量',
    '被过滤掉读段数的比例','怀孕次数', '生产次数', '胎儿是否健康']

liuying[col] = liuying[col].astype(float)

#IOR异常值删除
Q1 = liuying['孕妇BMI'].quantile(0.25)
Q3 = liuying['孕妇BMI'].quantile(0.75)

IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
liuying = liuying[(liuying['孕妇BMI'] >= lower_bound) & (liuying['孕妇BMI'] <= upper_bound)]


#GC删除不准确
# df = df[(df['GC含量'] >= 0.4) & (df['GC含量'] <= 0.6)]


# 删除Z值不准确
# df = df[(df['13号染色体的Z值'] >= -2.5) & (df['13号染色体的Z值'] <= 2.5)]
# df = df[(df['18号染色体的Z值'] >= -2.5) & (df['18号染色体的Z值'] <= 2.5)]
# df = df[(df['21号染色体的Z值'] >= -2.5) & (df['21号染色体的Z值'] <= 2.5)]
# df = df[(df['X染色体的Z值'] >= -2.5) & (df['X染色体的Z值'] <= 2.5)]
# df = df[(df['Y染色体的Z值'] >= -2.5) & (df['Y染色体的Z值'] <= 2.5)]


liuying = liuying.drop_duplicates(subset=['孕妇代码'])

#统计
print("统计:")
print(liuying.info())

print(liuying['Y染色体浓度'].describe())

a = 0.04

count_below_threshold = (liuying['Y染色体浓度'] < a).sum()

print(f"小于 {a} 的元素个数为：{count_below_threshold}")

# #周化
# df['检测孕周'] = df['检测孕周']/7

liuying.to_excel('处理后数据.xlsx')
