# douban_top250_full.py
# -*- coding: utf-8 -*-
"""
豆瓣电影 Top250 完整字段爬虫 + 清洗 + 可视化
"""
import time
import random
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from bs4 import BeautifulSoup

# ---------- 参数 ----------
BASE_URL = "https://movie.douban.com/top250"
COOKIE = "bid=uDVcMWuC9GE; douban-fav-remind=1; _pk_id.100001.4cf6=fdfd2315debc6fe9.1765964658.; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __yadk_uid=GflqLzU6Ds9gy7Av2HulykCgPQm38w6l"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "Referer": "https://movie.douban.com/top250",
}
MIN_SCORE = 8.5
START_PAGE, END_PAGE = 0, 9
CSV_NAME = "douban_top250_8.5+.csv"
XLSX_NAME = "douban_top250_8.5+.xlsx"

sns.set_style("whitegrid")
rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


# ---------- 抓取 ----------
def fetch_one_page(start: int):
    url = f"{BASE_URL}?start={start}"
    print(f"[+] 抓取 {url}")
    resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=False)
    if resp.status_code != 200:
        raise RuntimeError(f"状态码 {resp.status_code}")
    soup = BeautifulSoup(resp.text, "lxml")
    items = soup.select("div.item")
    data = []
    for it in items:
        # 1. 名称
        title = it.select_one("span.title").get_text(strip=True)
        # 2. 评分
        rating = float(it.select_one("span.rating_num").text)
        # 3. 评价人数
        comment_node = it.find("span", string=lambda x: x and "人评价" in x)
        comment_num = int(comment_node.text.replace("人评价", "").strip()) if comment_node else 0
        # 4. 年份/国家/类型/导演/主演
        info_node = it.select_one("div.bd p:first-child")
        year, country, genre, director, actors = None, None, None, None, None
        if info_node:
            lines = [line.strip() for line in info_node.get_text().split("\n") if line.strip()]
            # 最后一行格式：1994 / 美国 / 犯罪 剧情
            if len(lines) >= 2:
                meta = lines[-1].split("/")
                if len(meta) == 3:
                    try:
                        year = int(meta[0].strip())
                        country = meta[1].strip()
                        genre = [g.strip() for g in meta[2].split()]
                    except Exception:
                        pass
                # 第一行：导演: 弗兰克·德拉邦特 Frank Darabont   主演: 蒂姆·罗宾斯 ...
                first_line = lines[0]
                if "导演:" in first_line and "主演:" in first_line:
                    parts = first_line.split("主演:")
                    director = parts[0].replace("导演:", "").strip()
                    actors = parts[1].strip() if len(parts) > 1 else None
        # 5. 简介
        quote_node = it.select_one("p.quote span")
        quote = quote_node.text.strip() if quote_node else None

        data.append({
            "电影名称": title,
            "评价人数": comment_num,
            "上映年份": year,
            "电影类型": genre,
            "导演/主演": f"{director} / {actors}" if director and actors else director,
            "剧情简介": quote,
        })
    return data


def crawl_all():
    all_data = []
    for p in range(START_PAGE, END_PAGE + 1):
        start = p * 25
        try:
            all_data.extend(fetch_one_page(start))
        except Exception as e:
            print(f"[!] 第 {p} 页失败: {e}")
        time.sleep(random.uniform(1.5, 2.5))
    df = pd.DataFrame(all_data)
    print(f"[+] 原始抓取 {len(df)} 条")
    return df


# ---------- 清洗 ----------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # 评分≥8.5
    df = df[df["评分"] >= MIN_SCORE].copy()
    df = df.dropna(subset=["电影名称"])
    df = df.drop_duplicates(subset=["电影名称"])
    # 空列表转字符串
    df["电影类型"] = df["电影类型"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "未知")
    df["上映年份"] = df["上映年份"].fillna(0).astype(int)
    print(f"[+] 清洗后剩余 {len(df)} 条")
    return df.reset_index(drop=True)


# ---------- 保存 ----------
def save_files(df: pd.DataFrame):
    df.to_csv(CSV_NAME, index=False, encoding="utf-8-sig")
    df.to_excel(XLSX_NAME, index=False)
    print(f"[+] 已保存 {CSV_NAME} & {XLSX_NAME}")



# ---------- 可视化（4 张核心图） ----------
def plot_year_dist(df: pd.DataFrame):
    """1. 高分电影年份分布柱状图"""
    plt.figure(figsize=(12, 5))
    year_counts = df["上映年份"].value_counts().sort_index()
    sns.barplot(x=year_counts.index.astype(str), y=year_counts.values,
                hue=year_counts.index.astype(str), palette="Blues_d", legend=False)
    plt.title("高分电影(≥8.5)年份分布", fontsize=14)
    plt.ylabel("部数")
    plt.xlabel("年份")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("1_年份分布.png", dpi=300)
    plt.close()


def plot_genre(df: pd.DataFrame):
    """2. 电影类型占比饼图"""
    genre_list = [g.strip() for sub in df["电影类型"].dropna() for g in sub.split(",")]
    genre_counts = pd.Series(genre_list).value_counts().head(10)
    plt.figure(figsize=(8, 8))
    plt.pie(genre_counts.values, labels=genre_counts.index, autopct="%1.1f%%",
            startangle=90, colors=sns.color_palette("Set3", len(genre_counts)))
    plt.title("高分电影类型占比 Top10", fontsize=14)
    plt.savefig("2_类型占比饼图.png", dpi=300)
    plt.close()


def plot_score_vs_comments(df: pd.DataFrame):
    """3. 评分 vs 评价人数散点图"""
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="评分", y="评价人数", hue="评分",
                    palette="coolwarm", s=60, edgecolor=None, legend=False)
    plt.title("评分与评价人数相关性", fontsize=14)
    plt.xlabel("评分")
    plt.ylabel("评价人数")
    plt.tight_layout()
    plt.savefig("3_评分评价人数散点图.png", dpi=300)
    plt.close()


def plot_top10(df: pd.DataFrame):
    """4. Top10高分电影条形图"""
    top10 = df.nlargest(10, "评分")[["电影名称", "评分"]]
    plt.figure(figsize=(8, 6))
    sns.barplot(y=top10["电影名称"], x=top10["评分"], hue=top10["电影名称"],
                palette="Reds_r", legend=False)
    plt.title("Top10 高分电影", fontsize=14)
    plt.xlabel("评分")
    plt.tight_layout()
    plt.savefig("4_Top10条形图.png", dpi=300)
    plt.close()
# ---------- main ----------
def main():
    print("========== 豆瓣 Top250 完整字段爬虫开始 ==========")
    raw_df = crawl_all()
    clean_df = clean_data(raw_df)
    save_files(clean_df)
    plot_year_dist(clean_df)
    plot_genre(clean_df)
    plot_score_vs_comments(clean_df)
    plot_top10(clean_df)
    print("========== 4 张核心图表已生成 ==========")


if __name__ == "__main__":
    main()