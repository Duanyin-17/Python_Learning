import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取数据
df = pd.read_csv('data_zh.csv')

# 2. 将日期列转换为 datetime 类型，无法解析的设置为 NaT
df['日期'] = pd.to_datetime(df['日期'], format='%m/%d/%Y', errors='coerce')

# 3. 检查无效日期
if df['日期'].isna().any():
    print("存在无效日期，已将其设置为 NaT。")
    print("无效日期的行：")
    print(df[df['日期'].isna()])

# 4. 删除无效日期的行
df = df.dropna(subset=['日期'])

# 5. 按日期排序
df = df.sort_values('日期')

# 6. 基本统计量计算
gold_price = df['收盘价']
gold_stats = {
    '均值': gold_price.mean(),
    '中位数': gold_price.median(),
    '标准差': gold_price.std(),
    '最小值': gold_price.min(),
    '最大值': gold_price.max()
}

print("\n黄金价格基本统计量：")
for key, value in gold_stats.items():
    print(f"{key}: {value:.2f}")

# 7. 绘制黄金价格随时间变化的折线图
plt.figure(figsize=(14, 6))
plt.plot(df['日期'], gold_price, color='gold', linewidth=1.5)

# 优化 X 轴的时间显示
plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # 每年显示一次
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # 显示年份
plt.gcf().autofmt_xdate()  # 自动旋转日期标签

plt.title('黄金价格随时间变化趋势')
plt.xlabel('日期')
plt.ylabel('收盘价 (美元)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# 8. 分时间段波动分析
# 添加年、季度、月列
df['年'] = df['日期'].dt.year
df['季度'] = df['日期'].dt.quarter
df['月'] = df['日期'].dt.month

# 按年分析
yearly_stats = df.groupby('年')['收盘价'].agg(['mean', 'std', 'min', 'max'])
yearly_stats['波动幅度'] = yearly_stats['max'] - yearly_stats['min']
print("\n按年波动分析：")
print(yearly_stats)

# 按季度分析
quarterly_stats = df.groupby(['年', '季度'])['收盘价'].agg(['mean', 'std', 'min', 'max'])
quarterly_stats['波动幅度'] = quarterly_stats['max'] - quarterly_stats['min']
print("\n按季度波动分析（前10行）：")
print(quarterly_stats.head(10))

# 按月分析
monthly_stats = df.groupby(['年', '月'])['收盘价'].agg(['mean', 'std', 'min', 'max'])
monthly_stats['波动幅度'] = monthly_stats['max'] - monthly_stats['min']
print("\n按月波动分析（前10行）：")
print(monthly_stats.head(10))