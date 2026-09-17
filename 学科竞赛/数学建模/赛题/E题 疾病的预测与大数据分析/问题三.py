import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def predict_individual_comorbidity_probabilities():
    """预测每个样本的共病概率"""

    # 1. 加载数据
    stroke_df = pd.read_csv('stroke_t.csv').dropna()
    heart_df = pd.read_csv('heart_t.csv').dropna()
    cirrhosis_df = pd.read_csv('cirrhosis_t.csv').dropna()

    print(f"数据集样本数: Stroke={len(stroke_df)}, Heart={len(heart_df)}, Cirrhosis={len(cirrhosis_df)}")

    # 2. 特征对齐（简化版）
    def prepare_features(df, dataset_type):
        """为不同数据集准备特征"""
        features = {}

        # 年龄特征
        if 'age' in df.columns:
            features['age'] = df['age'].values
        elif 'Age' in df.columns:
            if dataset_type == 'cirrhosis':
                features['age'] = df['Age'].values / 365.25  # 天转年
            else:
                features['age'] = df['Age'].values

        # 高血压相关
        if 'hypertension' in df.columns:
            features['hypertension'] = df['hypertension'].values
        elif 'RestingBP' in df.columns:
            features['hypertension'] = (df['RestingBP'] > 140).astype(int).values

        # 胆固醇
        if 'Cholesterol' in df.columns:
            features['cholesterol'] = df['Cholesterol'].values

        # 血糖相关
        if 'avg_glucose_level' in df.columns:
            features['glucose'] = df['avg_glucose_level'].values
        elif 'FastingBS' in df.columns:
            features['glucose'] = df['FastingBS'].values

        # BMI
        if 'bmi' in df.columns:
            features['bmi'] = df['bmi'].values

        # 转换为DataFrame
        features_df = pd.DataFrame(features)

        # 填充缺失值
        for col in features_df.columns:
            if features_df[col].isnull().any():
                features_df[col] = features_df[col].fillna(features_df[col].mean())

        return features_df

    # 准备特征
    stroke_features = prepare_features(stroke_df, 'stroke')
    heart_features = prepare_features(heart_df, 'heart')
    cirrhosis_features = prepare_features(cirrhosis_df, 'cirrhosis')

    # 获取目标变量
    stroke_y = stroke_df['stroke'].values
    heart_y = heart_df['HeartDisease'].values
    cirrhosis_y = (cirrhosis_df['Stage'] >= 3).astype(int).values  # 阶段3-4视为患病

    # 3. 找到所有数据集的共同特征
    all_features = set(stroke_features.columns) | set(heart_features.columns) | set(cirrhosis_features.columns)
    common_features = sorted(all_features)
    print(f"共同特征: {common_features}")

    # 4. 为每个数据集对齐特征（填充缺失特征）
    def align_features(features_df, common_features):
        """对齐特征到共同特征空间"""
        aligned_df = pd.DataFrame(index=features_df.index)

        for feat in common_features:
            if feat in features_df.columns:
                aligned_df[feat] = features_df[feat]
            else:
                # 如果特征缺失，用0填充（后续会标准化）
                aligned_df[feat] = 0

        return aligned_df

    stroke_X_aligned = align_features(stroke_features, common_features)
    heart_X_aligned = align_features(heart_features, common_features)
    cirrhosis_X_aligned = align_features(cirrhosis_features, common_features)

    # 5. 标准化特征
    scaler = StandardScaler()
    stroke_X_scaled = scaler.fit_transform(stroke_X_aligned)
    heart_X_scaled = scaler.transform(heart_X_aligned)
    cirrhosis_X_scaled = scaler.transform(cirrhosis_X_aligned)

    # 6. 训练三个疾病模型
    models = {}

    # 中风模型
    stroke_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    stroke_model.fit(stroke_X_scaled, stroke_y)
    models['stroke'] = stroke_model

    # 心脏病模型
    heart_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    heart_model.fit(heart_X_scaled, heart_y)
    models['heart'] = heart_model

    # 肝硬化模型
    cirrhosis_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    cirrhosis_model.fit(cirrhosis_X_scaled, cirrhosis_y)
    models['cirrhosis'] = cirrhosis_model

    # 7. 为每个数据集的每个样本预测共病概率
    def predict_comorbidity_for_dataset(X, dataset_name, models):
        """为某个数据集的所有样本预测共病概率"""
        probs = {}

        # 预测单疾病概率
        probs['stroke'] = models['stroke'].predict_proba(X)[:, 1]
        probs['heart'] = models['heart'].predict_proba(X)[:, 1]
        probs['cirrhosis'] = models['cirrhosis'].predict_proba(X)[:, 1]

        # 计算共病概率
        n_samples = len(X)
        comorbidity_results = []

        for i in range(n_samples):
            p_stroke = probs['stroke'][i]
            p_heart = probs['heart'][i]
            p_cirrhosis = probs['cirrhosis'][i]

            individual_probs = {
                'dataset': dataset_name,
                'sample_id': i,
                'p_stroke': p_stroke,
                'p_heart': p_heart,
                'p_cirrhosis': p_cirrhosis,
                'p_stroke_heart': p_stroke * p_heart,
                'p_stroke_cirrhosis': p_stroke * p_cirrhosis,
                'p_heart_cirrhosis': p_heart * p_cirrhosis,
                'p_all_three': p_stroke * p_heart * p_cirrhosis,
                'high_risk_stroke_heart': p_stroke * p_heart > 0.25,
                'high_risk_all_three': p_stroke * p_heart * p_cirrhosis > 0.1
            }
            comorbidity_results.append(individual_probs)

        return pd.DataFrame(comorbidity_results)

    # 为三个数据集分别预测
    stroke_comorbidity = predict_comorbidity_for_dataset(stroke_X_scaled, 'stroke', models)
    heart_comorbidity = predict_comorbidity_for_dataset(heart_X_scaled, 'heart', models)
    cirrhosis_comorbidity = predict_comorbidity_for_dataset(cirrhosis_X_scaled, 'cirrhosis', models)

    # 合并结果
    all_comorbidity = pd.concat([stroke_comorbidity, heart_comorbidity, cirrhosis_comorbidity], ignore_index=True)

    # 8. 保存结果
    all_comorbidity.to_csv('individual_comorbidity_probabilities.csv', index=False)

    # 9. 分析结果
    print("\n每个样本的共病概率统计:")
    print("=" * 50)
    print(f"总样本数: {len(all_comorbidity)}")
    print(
        f"高中风+心脏病风险样本: {all_comorbidity['high_risk_stroke_heart'].sum()} ({all_comorbidity['high_risk_stroke_heart'].mean():.2%})")
    print(
        f"高三疾病风险样本: {all_comorbidity['high_risk_all_three'].sum()} ({all_comorbidity['high_risk_all_three'].mean():.2%})")

    print("\n平均概率:")
    print(f"中风概率: {all_comorbidity['p_stroke'].mean():.4f}")
    print(f"心脏病概率: {all_comorbidity['p_heart'].mean():.4f}")
    print(f"肝硬化概率: {all_comorbidity['p_cirrhosis'].mean():.4f}")
    print(f"中风+心脏病共病概率: {all_comorbidity['p_stroke_heart'].mean():.4f}")
    print(f"三种疾病共病概率: {all_comorbidity['p_all_three'].mean():.4f}")

    # 10. 可视化高风险人群特征
    high_risk_df = all_comorbidity[all_comorbidity['high_risk_all_three']]

    if len(high_risk_df) > 0:
        plt.figure(figsize=(12, 8))

        # 高风险人群的概率分布
        plt.subplot(2, 2, 1)
        plt.hist(high_risk_df['p_all_three'], bins=20, alpha=0.7, color='red')
        plt.title('高风险人群的三疾病共病概率分布')
        plt.xlabel('P(三种疾病)')
        plt.ylabel('频数')

        # 各数据集的high risk比例
        plt.subplot(2, 2, 2)
        risk_by_dataset = all_comorbidity.groupby('dataset')['high_risk_all_three'].mean()
        risk_by_dataset.plot(kind='bar', color=['skyblue', 'lightgreen', 'salmon'])
        plt.title('各数据集的高风险人群比例')
        plt.ylabel('高风险比例')

        # 特征与共病概率的关系（示例：年龄）
        plt.subplot(2, 2, 3)
        # 这里需要原始特征数据，简化处理
        plt.scatter(stroke_X_aligned['age'], stroke_comorbidity['p_all_three'], alpha=0.5)
        plt.title('年龄与三疾病共病概率的关系')
        plt.xlabel('年龄')
        plt.ylabel('P(三种疾病)')

        plt.tight_layout()
        plt.savefig('individual_risk_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

    return all_comorbidity, models, scaler, common_features


# 运行函数
individual_probs, models, scaler, feature_names = predict_individual_comorbidity_probabilities()


# 示例：为新样本预测共病概率
def predict_new_sample(models, scaler, feature_names, new_features):
    """为新样本预测共病概率"""
    # 确保特征顺序一致
    new_df = pd.DataFrame([new_features], columns=feature_names)
    new_scaled = scaler.transform(new_df)

    probs = {
        'stroke': models['stroke'].predict_proba(new_scaled)[0, 1],
        'heart': models['heart'].predict_proba(new_scaled)[0, 1],
        'cirrhosis': models['cirrhosis'].predict_proba(new_scaled)[0, 1]
    }

    # 计算共病概率
    result = {
        **probs,
        'stroke_heart': probs['stroke'] * probs['heart'],
        'stroke_cirrhosis': probs['stroke'] * probs['cirrhosis'],
        'heart_cirrhosis': probs['heart'] * probs['cirrhosis'],
        'all_three': probs['stroke'] * probs['heart'] * probs['cirrhosis']
    }

    return result


# 使用示例
print("\n新样本预测示例:")
sample_features = {
    'age': 65,
    'hypertension': 1,
    'cholesterol': 280,
    'glucose': 150,
    'bmi': 32
}

sample_prediction = predict_new_sample(models, scaler, feature_names, sample_features)
for disease, prob in sample_prediction.items():
    print(f"{disease}: {prob:.4f}")