import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.impute import SimpleImputer
import logging
from typing import Tuple, Dict

'''
由于问题二SVM模型的图像无法正常生成，请查看问题二（SVM）以获取图像
'''

# 配置设置
class Config:
    NUMERIC_FEATURES = ['年龄']
    CATEGORICAL_FEATURES = ['婚姻状态', '教育程度', '政治面貌', '文化程度']
    MODELS = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'SVM': SVC(kernel='linear', random_state=42, probability=True)
    }
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    PLOT_TOP_N_FEATURES = 10

def setup_environment():
    try:
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        sns.set_style("whitegrid", {'font.sans-serif': ['Microsoft YaHei', 'SimHei']})
    except:
        logging.warning("未找到中文字体，图表可能无法正常显示中文")
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_preprocessor() -> ColumnTransformer:
    #创建数据预处理管道
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    return ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, Config.NUMERIC_FEATURES),
            ('cat', categorical_transformer, Config.CATEGORICAL_FEATURES)
        ]
    )


def get_feature_importance(model, preprocessor) -> pd.DataFrame:
    try:
        # 获取特征名称
        numeric_features = Config.NUMERIC_FEATURES
        onehot_encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
        categorical_features = preprocessor.named_transformers_['cat'].feature_names_in_
        categorical_feature_names = onehot_encoder.get_feature_names_out(categorical_features)
        feature_names = numeric_features + list(categorical_feature_names)

        # 提取重要性分数并确保为float类型
        if isinstance(model, SVC):
            if hasattr(model, 'coef_'):
                importance = np.abs(model.coef_[0]).astype(float)
            else:
                return pd.DataFrame()
        elif hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_.astype(float)
        elif hasattr(model, 'coef_'):
            importance = np.abs(model.coef_[0]).astype(float)
        else:
            return pd.DataFrame()

        # 创建特征重要性数据框
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importance
        })

        # 对分类特征进行聚合
        aggregated_importance = pd.DataFrame()
        for numeric_feature in numeric_features:
            aggregated_importance = pd.concat([
                aggregated_importance,
                importance_df[importance_df['Feature'] == numeric_feature][['Feature', 'Importance']]
            ])

        for categorical_feature in Config.CATEGORICAL_FEATURES:
            categorical_importance = importance_df[importance_df['Feature'].str.startswith(categorical_feature)]
            aggregated_importance = pd.concat([
                aggregated_importance,
                pd.DataFrame({
                    'Feature': [categorical_feature],
                    'Importance': [categorical_importance['Importance'].sum()]
                })
            ])

        return aggregated_importance.sort_values(by='Importance', ascending=False).reset_index(drop=True)
    except Exception as e:
        logging.error(f"获取特征重要性时出错: {str(e)}")
        return pd.DataFrame()

def plot_feature_importance(importance_df: pd.DataFrame, model_name: str):
    try:
        # 检查数据是否有效
        if importance_df.empty or 'Importance' not in importance_df.columns:
            logging.warning(f"{model_name} 的特征重要性数据无效")
            return

        importance_df['Importance'] = pd.to_numeric(importance_df['Importance'], errors='coerce')

        # 按重要性排序并绘图
        if 'Importance' in importance_df.columns:
            importance_df = importance_df.nlargest(Config.PLOT_TOP_N_FEATURES, 'Importance')
            plt.figure(figsize=(10, len(importance_df) / 2))
            sns.barplot(x='Importance', y='Feature', data=importance_df)
            plt.title(f'{model_name} - 特征重要性')
            plt.tight_layout()
            plt.show()
        else:
            logging.error("列 'Importance' 不存在于数据框中")
    except Exception as e:
        logging.error(f"绘制特征重要性图表时出错: {str(e)}")

def evaluate_model(pipeline, X_test, y_test) -> Dict[str, float]:
    y_pred = pipeline.predict(X_test)
    return {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1 Score': f1_score(y_test, y_pred)
    }

def train_and_evaluate_models(
        X: pd.DataFrame,
        y: pd.Series,
        prediction_df: pd.DataFrame
) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=Config.TEST_SIZE,
        random_state=Config.RANDOM_STATE
    )

    preprocessor = create_preprocessor()
    results = []
    feature_importance_results = {}

    for name, model in Config.MODELS.items():
        try:
            logging.info(f"开始训练 {name}...")

            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', model)
            ])
            pipeline.fit(X_train, y_train)

            metrics = evaluate_model(pipeline, X_test, y_test)
            metrics['Model'] = name
            results.append(metrics)

            prediction_df[f'{name}_预测结果'] = pipeline.predict(prediction_df)
            prediction_df.to_excel(f"{name}_预测结果.xlsx", index=False)
            logging.info(f"{name} 预测结果已保存")

            importance_df = get_feature_importance(pipeline.named_steps['classifier'], preprocessor)
            feature_importance_results[name] = importance_df

            plot_feature_importance(importance_df, name)

            logging.info(f"{name} 训练和评估完成")

        except Exception as e:
            logging.error(f"训练 {name} 时出错: {str(e)}")

    return pd.DataFrame(results), feature_importance_results

def main():
    setup_environment()

    try:
        logging.info("正在读取数据...")
        df = pd.read_excel("就失业状态分析结果1.xlsx")
        prediction_df = pd.read_excel("附件1 数据-C题.xls", sheet_name="预测集", skiprows=1)

        X = df[Config.NUMERIC_FEATURES + Config.CATEGORICAL_FEATURES]
        y = df['就业状态']

        results_df, feature_importance = train_and_evaluate_models(X, y, prediction_df)

        results_df.to_excel("模型评估结果.xlsx", index=False)
        logging.info("\n模型评估结果:")
        print(results_df.to_string())

    except Exception as e:
        logging.error(f"程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()