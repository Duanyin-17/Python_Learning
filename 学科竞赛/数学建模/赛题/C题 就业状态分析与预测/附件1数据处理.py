import pandas as pd
import matplotlib.pyplot as plt

file_path = r"附件1 数据-C题.xls"

# 读取行业代码数据
sheet3 = pd.read_excel(file_path, sheet_name='行业代码')
valid_industry_codes = set(sheet3.iloc[:, 0].dropna().astype(str))

df = pd.read_excel(file_path,skiprows=2)
#print("原始数据列名：", df.columns)  # 打印列名

# 删除缺失关键字段的样本
df = df.dropna(subset=['户籍地址', '专业', '毕业学校'])

# 检查并删除重复数据
df = df.drop_duplicates()

# 验证清洗结果
print(df.shape)

# 就失业状态
def is_employed(row):
    # 就业条件
    employment_conditions = (
            pd.notna(row['就业时间']) and
            pd.notna(row['录用单位编号']) and
            row['是否签订劳动合同'] == '1' and
            row['行业代码'] in valid_industry_codes
    )

    # 失业条件
    unemployment_conditions = (
            row['失业注销时间'] ==r'\N' or
            row['失业注销时间'] < row['失业时间'] or
            row['登记就失业状态'] == '0'
    )

    if unemployment_conditions:
        return 0
    elif employment_conditions:
        return 1
    else:
        return 0


df["就业状态"] = df.apply(is_employed, axis=1)

#print(df[["人员编11号", "姓名", "就业状态"]])

#整理新表特征
columns_to_extract = ['姓名','性别','生日','年龄','民族','婚姻状态','教育程度','政治面貌','户籍地址',
                      '专业','宗教信仰','户口性质','户口所在地区（代码）','户口所在地区（名称）','文化程度',
                      '毕业学校','毕业日期','所学专业代码','所学专业名称','人口类型','兵役状态','是否残疾人',
                      '是否青少年','是否老年人','变动类型','是否独居','居住状态','就业状态']

# 确定映射
gender_mapping = {0:"未知",1: "男",2: "女",9: "未说明"}
marital_status_mapping = {10: "未婚",20: "已婚",21: "初婚",22: "再婚",23: "复婚",30: "丧偶",40: "离婚"}
education_level_mapping = {
    10: "研究生教育", 11: "博士研究生毕业",12: "博士研究生结业", 13: "博士研究生肄业",
    14: "硕士研究生毕业", 15: "硕士研究生结业", 16: "硕士研究生肄业", 17: "研究生班毕业",
    18: "研究生班结业", 19: "研究生班肄业", 20: "大学本科教育",21: "大学本科毕业",
    22: "大学本科结业", 23: "大学本科肄业", 28: "大学普通班毕业", 30: "大学专科教育",
    31: "大学专科毕业", 32: "大学专科结业", 33: "大学专科肄业", 40: "中等职业教育",
    41: "中等专科毕业", 42: "中等专科结业", 43: "中等专科肄业", 44: "职业高中毕业",
    45: "职业高中结业", 46: "职业高中肄业", 47: "技工学校毕业", 48: "技工学校结业",
    49: "技工学校肄业", 50: "高中以下", 60: "普通高级中学教育", 61: "普通高中毕业",
    62: "普通高中结业", 63: "普通高中肄业", 70: "初级中学教育", 71: "初中毕业",
    73: "初中肄业", 80: "小学教育", 81: "小学毕业", 83: "小学肄业",
    90: "文盲或半文盲", 91: "中等师范学校（幼儿师范学校）毕业", 92: "中等师范学校（幼儿师范学校）结业",
    93: "中等师范学校（幼儿师范学校）肄业", 99: "其他"
}
culture_level_mapping = {"31": "大学专科","44": "职业高中", "47": "技工学校","11": "博士研究生","21": "大学本科",
                         "61": "普通中学", "14": "硕士研究生", "41": "中等专科","90": "其他","71": "初级中学","81": "小学"}
political_affiliation_mapping = {0: "群众",1: "中国共产党党员",10: "九三学社社员",11: "台湾民主自治同盟盟员",12: "无党派民主人士",
                                 2: "中国共产党预备党员",3: "中国共产主义青年团团员",4: "中国国民党革命委员会会员",5: "中国民主同盟盟员",
                                 6: "中国民主建国会会员",7: "中国民主促进会会员",8: "中国农工民主党党员",9: "中国致公党党员"
}
occupation_mapping = {"10000": "管理人员","10100": "管理人员","10200": "管理人员","10300": "管理人员","10400": "管理人员",
                      "10500": "管理人员","10600": "管理人员","20000": "技术人员","20100": "技术人员","20200": "技术人员",
                      "20300": "技术人员","20400": "技术人员","20500": "技术人员","20600": "技术人员","20700": "技术人员",
                      "20800": "技术人员","20900": "技术人员","21000": "技术人员","29900": "技术人员","30000": "办事人员",
                      "30100": "办事人员","30200": "办事人员","39900": "办事人员","40000": "服务人员","40100": "服务人员",
                      "40200": "服务人员","40300": "服务人员","40400": "服务人员","40500": "服务人员","40600": "服务人员",
                      "40700": "服务人员","40800": "服务人员","40900": "服务人员","41000": "服务人员","41100": "服务人员",
                      "41200": "服务人员","41300": "服务人员","41400": "服务人员","49900": "服务人员","50000": "农业人员",
                      "50100": "农业人员","50200": "农业人员","50300": "农业人员","50400": "农业人员","50500": "农业人员",
                      "59900": "农业人员","60000": "制造业人员","60100": "制造业人员","60200": "制造业人员","60300": "制造业人员",
                      "60400": "制造业人员","60500": "制造业人员","60600": "制造业人员","60700": "制造业人员","60800": "制造业人员",
                      "60900": "制造业人员","61000": "制造业人员","61100": "制造业人员","61200": "制造业人员","61300": "制造业人员",
                      "61400": "制造业人员","61500": "制造业人员","61600": "制造业人员","61700": "制造业人员","61800": "制造业人员",
                      "61900": "制造业人员","62000": "制造业人员","62100": "制造业人员","62200": "制造业人员","62300": "制造业人员",
                      "62400": "制造业人员","62500": "制造业人员","62600": "制造业人员","62700": "制造业人员","62800": "制造业人员",
                      "62900": "制造业人员","63000": "制造业人员","63100": "制造业人员","69900": "制造业人员","70000": "军人",
                      "80000": "不便分类","90000": "未从业","90001": "在读学生","90002": "离退休人员"
}

# 修改映射
df['性别']=df['性别'].map(gender_mapping)
df['婚姻状态'] = df['婚姻状态'].map(marital_status_mapping)
df['教育程度'] = df['教育程度'].map(education_level_mapping)
df['文化程度'] = df['文化程度'].map(culture_level_mapping)
df['政治面貌'] = df['政治面貌'].map(political_affiliation_mapping).fillna("未知")
# 函数：将多个代码映射为多个描述
def map_codes_to_descriptions(codes_str, mapping):
    codes = codes_str.split(',')
    descriptions = [mapping.get(code.strip(), '未知') for code in codes]
    return ', '.join(descriptions)

# 应用映射函数到 '专业' 字段
df['专业描述'] = df['专业'].apply(lambda x: map_codes_to_descriptions(x, occupation_mapping))

# 将专业代码转换为专业描述
df['专业'] = df['专业'].apply(lambda x: ', '.join([occupation_mapping.get(i, '未知') for i in x.split(',')]))



# 保存
new_data = df[columns_to_extract]
new_data.to_excel(r"就失业状态分析结果1.xlsx", index=False)



employment_mapping = {1: "就业", 0: "失业"}
df['就业状态'] = df['就业状态'].map(employment_mapping)

# 整体就业状态分析
employment_status = df['就业状态'].value_counts()
print("整体就业状态分析：")
print(employment_status)
print()

#中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 按性别分析就业状态
gender_employment = df.groupby('性别')['就业状态'].value_counts().unstack().fillna(0)
print("按性别分析就业状态：")
print(gender_employment)
print()

# 绘制按性别分析的柱状图
gender_employment.plot(kind='bar', stacked=True)
plt.title('按性别分析就业状态')
plt.xlabel('性别')
plt.xticks(rotation=0)
plt.ylabel('人数')
plt.legend(title='就业状态')
plt.show()

# 按年龄段分析就业状态
df['年龄段'] = pd.cut(df['年龄'], bins=[20, 30, 40, 50, 60, 70, 80], right=False)
age_group_employment = df.groupby('年龄段', observed=False)['就业状态'].value_counts().unstack().fillna(0)
print("按年龄段分析就业状态：")
print(age_group_employment)
print()

# 绘制按年龄段分析的柱状图
age_group_employment.plot(kind='bar', stacked=True)
plt.title('按年龄段分析就业状态')
plt.xlabel('年龄段')
plt.xticks(rotation=0)
plt.ylabel('人数')
plt.legend(title='就业状态')
plt.show()

# 按学历分析就业状态
education_employment = df.groupby('文化程度')['就业状态'].value_counts().unstack().fillna(0)
print("按文化程度分析就业状态：")
print(education_employment)
print()

# 绘制按学历分析的柱状图
education_employment.plot(kind='bar', stacked=True)
plt.title('按文化程度分析就业状态')
plt.xlabel('文化程度')
plt.xticks(rotation=0)
plt.ylabel('人数')
plt.legend(title='就业状态')
plt.show()

# 按专业分析就业状态
major_employment = df.groupby('专业')['就业状态'].value_counts().unstack().fillna(0)
print("按专业分析就业状态：")
print(major_employment)

# 过滤掉所有就业状态都为零的条目
major_employment = major_employment.loc[(major_employment.sum(axis=1) > 0)]

# 绘制按专业分析的水平柱状图
major_employment.plot(kind='bar', stacked=True)
plt.title('按专业分析就业状态')
plt.xlabel('人数')
plt.xticks(rotation=45)
plt.ylabel('专业')
plt.legend(title='就业状态')
plt.show()