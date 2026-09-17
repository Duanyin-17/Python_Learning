import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_excel('处理后数据(女胎).xlsx')


df['const'] = 1

y = df['女胎异常']
X = df[['const','孕妇BMI','原始读段数','唯一比对的读段数','GC含量','重复读段的比例', '13号染色体的Z值', '18号染色体的Z值','21号染色体的Z值']]

logit_model = sm.Logit(y, X).fit()

print(logit_model.summary())



