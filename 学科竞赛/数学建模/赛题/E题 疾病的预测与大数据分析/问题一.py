import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# 加载数据集
stroke_df = pd.read_csv("C:\\Users\\27047\\Desktop\\stroke.csv")
heart_df = pd.read_csv("C:\\Users\\27047\\Desktop\\heart.csv")
cirrhosis_df = pd.read_csv("C:\\Users\\27047\\Desktop\\cirrhosis.csv")


print("\nStroke Data Info:")
print(stroke_df.info())
print(stroke_df.head())

print("\nHeart Data Info:")
print(heart_df.info())
print(heart_df.head())

print("\nCirrhosis Data Info:")
print(cirrhosis_df.info())
print(cirrhosis_df.head())

# 检查缺失值
print("Stroke Data Missing Values:")
print(stroke_df.isnull().sum())

print("\nHeart Data Missing Values:")
print(heart_df.isnull().sum())

print("\nCirrhosis Data Missing Values:")
print(cirrhosis_df.isnull().sum())

#把smoking_statu列中的未知也看作缺失值
stroke_df.loc[stroke_df['smoking_status'] == 'Unknown', 'smoking_status'] = np.nan

# 删除包含缺失值的行
stroke_df.dropna(inplace=True)
heart_df.dropna(inplace=True)
cirrhosis_df.dropna(inplace=True)

# 数据类型转换
stroke_df['gender'] = stroke_df['gender'].astype('category')
stroke_df['ever_married'] = stroke_df['ever_married'].astype('category')
stroke_df['work_type'] = stroke_df['work_type'].astype('category')
stroke_df['Residence_type'] = stroke_df['Residence_type'].astype('category')
# stroke_df['smoking_status'] = stroke_df['smoking_status'].astype('category')

heart_df['Sex'] = heart_df['Sex'].astype('category')
heart_df['ChestPainType'] = heart_df['ChestPainType'].astype('category')
heart_df['RestingECG'] = heart_df['RestingECG'].astype('category')
heart_df['ExerciseAngina'] = heart_df['ExerciseAngina'].astype('category')
heart_df['ST_Slope'] = heart_df['ST_Slope'].astype('category')

cirrhosis_df['Sex'] = cirrhosis_df['Sex'].astype('category')
cirrhosis_df['Status'] = cirrhosis_df['Status'].astype('category')
cirrhosis_df['Drug'] = cirrhosis_df['Drug'].astype('category')
cirrhosis_df['Ascites'] = cirrhosis_df['Ascites'].astype('category')
cirrhosis_df['Hepatomegaly'] = cirrhosis_df['Hepatomegaly'].astype('category')
cirrhosis_df['Spiders'] = cirrhosis_df['Spiders'].astype('category')
cirrhosis_df['Edema'] = cirrhosis_df['Edema'].astype('category')

smoking_status_mapping = {
    'formerly smoked': 1,
    'never smoked': 0,
    'smokes': 2,
}

stroke_df['smoking_status'] = stroke_df['smoking_status'].map(smoking_status_mapping)

# 使用 Label Encoding 转换所有分类变量
label_encoder = LabelEncoder()

for col in stroke_df.select_dtypes(include=['category']).columns:
    stroke_df[col] = label_encoder.fit_transform(stroke_df[col])

for col in heart_df.select_dtypes(include=['category']).columns:
    heart_df[col] = label_encoder.fit_transform(heart_df[col])

for col in cirrhosis_df.select_dtypes(include=['category']).columns:
    cirrhosis_df[col] = label_encoder.fit_transform(cirrhosis_df[col])

stroke_df.to_csv('stroke_t.csv')
heart_df.to_csv('heart_t.csv')
cirrhosis_df.to_csv('cirrhosis_t.csv')

# 描述性统计
print("Stroke Data Descriptive Statistics:")
descriptive_stroke_stats = stroke_df.describe()
print(descriptive_stroke_stats)
descriptive_stroke_stats.to_csv('descriptive_stroke_stats.csv')

print("\nHeart Data Descriptive Statistics:")
descriptive_heart_stats = heart_df.describe()
print(descriptive_heart_stats)
descriptive_heart_stats.to_csv('descriptive_heart_stats.csv')

print("\nCirrhosis Data Descriptive Statistics:")
descriptive_cirrhosis_stats = cirrhosis_df.describe()
print(descriptive_cirrhosis_stats)
descriptive_cirrhosis_stats.to_csv('descriptive_cirrhosis_stats.csv')

# 热力图
# Stroke Data
plt.figure(figsize=(12, 8))
sns.heatmap(stroke_df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap for Stroke Data')
plt.show()

# Heart Data
plt.figure(figsize=(12, 8))
sns.heatmap(heart_df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap for Heart Data')
plt.show()

# Cirrhosis Data
plt.figure(figsize=(12, 8))
sns.heatmap(cirrhosis_df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap for Cirrhosis Data')
plt.show()





