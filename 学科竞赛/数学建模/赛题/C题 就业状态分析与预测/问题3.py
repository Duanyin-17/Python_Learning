import pandas as pd
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

# 配置设置
class Config:
    NUMERIC_FEATURES = ['年龄', 'GNI', 'LaborForce', 'CPI', 'Population']
    CATEGORICAL_FEATURES = ['婚姻状态', '教育程度', '政治面貌', '宗教信仰', '文化程度']
    MODELS = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'SVM': SVC(kernel='linear', random_state=42, probability=True)
    }
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    PLOT_TOP_N_FEATURES = 10



def create_preprocessor() -> ColumnTransformer:

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
            prediction_df.to_excel(f"问题三{name}_预测结果.xlsx", index=False)
            logging.info(f"{name} 预测结果已保存")

        except Exception as e:
            logging.error(f"训练 {name} 时出错: {str(e)}")

    return pd.DataFrame(results), feature_importance_results

def main():

    try:
        logging.info("正在读取数据...")
        df = pd.read_excel("问题三数据.xlsx")
        prediction_df = pd.read_excel("问题三预测数据.xlsx")

        X = df[Config.NUMERIC_FEATURES + Config.CATEGORICAL_FEATURES]
        y = df['就业状态']

        results_df, feature_importance = train_and_evaluate_models(X, y, prediction_df)

        results_df.to_excel("问题三模型评估结果.xlsx", index=False)
        logging.info("\n模型评估结果:")
        print(results_df.to_string())

    except Exception as e:
        logging.error(f"程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()