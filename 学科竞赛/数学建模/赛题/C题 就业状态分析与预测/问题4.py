import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler



# 数据预处理
def preprocess_jobs(jobs_df):
    jobs_df['Skills_Industry'] = jobs_df['RequiredSkills'] + ' ' + jobs_df['Industry']
    scaler = MinMaxScaler()
    jobs_df['Salary_Normalized'] = scaler.fit_transform(jobs_df[['Salary']])
    education_map = {'Bachelor': 1, 'Master': 2, 'PhD': 3}
    jobs_df['Education_Encoded'] = jobs_df['EducationLevel'].map(education_map)
    return jobs_df


def preprocess_seekers(seekers_df):
    education_map = {'小学': 0, '初中': 1, '高中': 2, '中专': 3,
                     '大学专科': 4, '大学本科': 5, '硕士': 6, '博士': 7}
    seekers_df['Education_Encoded'] = seekers_df['文化程度'].map(education_map)
    seekers_df['专业'] = seekers_df['专业'].str.replace(', ', ' ')
    scaler = MinMaxScaler()
    seekers_df['Age_Normalized'] = scaler.fit_transform(seekers_df[['年龄']])
    return seekers_df


# 加载数据
jobs = preprocess_jobs(pd.read_excel('招聘数据.xlsx'))
job_seekers = preprocess_seekers(pd.read_excel(r"问题三数据.xlsx"))

# 特征工程
tfidf = TfidfVectorizer()
job_text_features = tfidf.fit_transform(jobs['Skills_Industry'])
job_numeric_features = jobs[['Salary_Normalized', 'Education_Encoded']].values


# 计算相似度的函数
def calculate_similarity(job_text, job_numeric, seeker_text, seeker_numeric):
    text_sim = cosine_similarity(seeker_text, job_text)
    numeric_sim = 1 / (1 + np.sqrt(np.sum((seeker_numeric[:, None] - job_numeric) ** 2, axis=2)))
    return 0.6 * text_sim + 0.4 * numeric_sim


# 推荐函数
def recommend_jobs(similarity_matrix, seekers_df, jobs_df, top_n=3):
    recommendations = []
    for i in range(len(seekers_df)):
        seeker = seekers_df.iloc[i]
        sim_scores = list(enumerate(similarity_matrix[i]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        for job_idx, score in sim_scores[:top_n]:
            job = jobs_df.iloc[job_idx]
            recommendations.append({
                'Seeker_ID': seeker['姓名'],
                'Seeker_Education': seeker['文化程度'],
                'Seeker_Skills': seeker['专业'],
                'Job_ID': job['JobID'],
                'Job_Title': job['JobCategory'],
                'Required_Skills': job['RequiredSkills'],
                'Industry': job['Industry'],
                'Salary': job['Salary'],
                'Match_Score': round(score, 4)
            })
    return pd.DataFrame(recommendations)



# 为失业人员单独推荐
unemployed = job_seekers[job_seekers['就业状态'] == 0].copy()

unemployed_text = tfidf.transform(unemployed['专业'])
unemployed_numeric = unemployed[['Education_Encoded', 'Age_Normalized']].values

unemployed_sim = calculate_similarity(
    job_text_features, job_numeric_features,
    unemployed_text, unemployed_numeric
)

# 确保索引正确
unemployed.reset_index(drop=True, inplace=True)
unemployed_recommendations = recommend_jobs(unemployed_sim, unemployed, jobs)
print("\n失业人员专项推荐:", unemployed_recommendations.shape)
print(unemployed_recommendations.head())




unemployed_recommendations.to_excel('失业人员推荐结果.xlsx', index=False)