import numpy as np
import jenkspy
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_excel("处理后数据.xlsx")
bmi_data = df["孕妇BMI"].values

k_list = [1,2,3,4,5,6]
total_var_list = []

n_cols = 2
n_rows = (len(k_list) + n_cols - 1) // n_cols
fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(20, 6 * n_rows))
axes = axes.flatten()

for idx, k in enumerate(k_list):
    breaks = jenkspy.jenks_breaks(bmi_data, n_classes=k)
    groups = pd.cut(bmi_data, bins=breaks, include_lowest=True)
    group_counts = groups.value_counts().sort_index()
    total_within_var = 0
    for interval in group_counts.index:
        group_data = bmi_data[(bmi_data >= interval.left) & (bmi_data <= interval.right)]
        total_within_var += np.var(group_data)
    total_var_list.append(round(total_within_var, 2))

    ax = axes[idx]
    colors = plt.cm.Blues(np.linspace(0.4, 0.8, k))
    bars = ax.bar(range(len(group_counts)), group_counts.values, color=colors, edgecolor='black', linewidth=0.5)

    ax.set_title(f'Jenks分组：k={k}组（总组内方差={total_within_var:.2f}）', fontsize=12, fontweight='bold')
    ax.set_xlabel('BMI分组区间', fontsize=10)
    ax.set_ylabel('样本量', fontsize=10)
    ax.set_xticks(range(len(group_counts)))

    ax.set_xticklabels([str(interval) for interval in group_counts.index], rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 0.5, f'{int(height)}', ha='center', va='bottom',
                fontsize=9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

for idx in range(len(k_list), len(axes)):
    axes[idx].axis('off')

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(k_list, total_var_list, marker='o', linewidth=2.5, markersize=8, color='#2E86AB', markerfacecolor='#A23B72')

for k, var in zip(k_list, total_var_list):
    plt.annotate(f'{var}', (k, var), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10,
                 fontweight='bold')

plt.title('总组内方差随分组数的变化', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('分组数', fontsize=12)
plt.ylabel('组内总方差', fontsize=12)
plt.xticks(k_list)
plt.grid(True, alpha=0.3, linestyle='--')

plt.show()

print("=" * 50)
print("多k值Jenks分组结果汇总")
print("=" * 50)
for k, var in zip(k_list, total_var_list):
    print(f"k={k}组：总组内方差={var:.2f}")
print("=" * 50)
min_var_idx = np.argmin(total_var_list)
best_k = k_list[min_var_idx]
best_var = total_var_list[min_var_idx]
print(f"最优分组数（总组内方差最小）：k={best_k}，总组内方差={best_var:.2f}")
print("=" * 50)