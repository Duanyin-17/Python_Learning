import pandas as pd

df = pd.read_excel('处理后数据.xlsx')

a = ((df['Y染色体浓度'] > 0.04).sum())/df.shape[0]
print(f"{a*100:.2f}%")


