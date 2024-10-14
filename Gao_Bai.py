import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import re

df = pd.read_excel('高百 (2).xls', engine='xlrd')
print("Data successfully read.")
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号


def pace_to_seconds(pace):
    minutes, seconds = map(float, pace.split(':'))
    return minutes * 60 + seconds


def seconds_to_pace(seconds):
    minutes = int(seconds // 60)  # 计算分钟
    remaining_seconds = int(seconds % 60)  # 计算剩余的秒数
    return f"{minutes}:{remaining_seconds:02d}"  # 格式化为 "分钟:秒"


df['配速（秒）'] = df['配速'].apply(pace_to_seconds)


def pic():
    universities = df['团队名称'].unique()

    for university in universities:

        university_data = df[df['团队名称'] == university]

        if university_data.empty:
            continue

            # 计算平均配速
        average_pace_seconds = university_data['配速（秒）'].mean()
        average_minutes = int(average_pace_seconds // 60)
        average_seconds = int(average_pace_seconds % 60)
        average_pace_str = f'{average_minutes:02d}:{average_seconds:02d}'

        # 绘制直方图
        plt.figure(figsize=(10, 6))
        counts, bin_edges = np.histogram(university_data['配速（秒）'], bins=10)

        plt.hist(university_data['配速（秒）'], bins=10, color='skyblue', alpha=0.6)

        # 显示每个区间的人数
        for count, edge in zip(counts, bin_edges[:-1]):
            center = edge + (bin_edges[1] - bin_edges[0]) / 2
            plt.text(center, count, str(count), ha='center', fontsize=10, color='black')

        plt.xticks(ticks=bin_edges, labels=[f"{int(edge // 60)}:{int(edge % 60):02d}" for edge in bin_edges],
                   rotation=45)

        plt.axvline(average_pace_seconds, color='red', linestyle='--', label=f'平均配速: {average_pace_str}')

        plt.title(f'{university} 选手配速的分布')
        plt.xlabel('配速（分钟:秒）')
        plt.ylabel('人数')
        plt.legend()

        plt.tight_layout()
        plt.show()


def ave():
    overall_avg_pace = df.groupby('团队名称')['配速（秒）'].mean().reset_index()
    overall_avg_pace['性别'] = '整体'

    # 计算男女分开后的平均配速
    avg_pace_gender = df.groupby(['团队名称', '性别'])['配速（秒）'].mean().reset_index()

    # 整合数据
    summary = pd.concat([
        overall_avg_pace,
        avg_pace_gender
    ])

    # 将数据重塑为大学为行，平均配速为列
    summary_pivot = summary.pivot(index='团队名称', columns='性别', values='配速（秒）').reset_index()

    # 填充 NaN 值
    summary_pivot.fillna(0, inplace=True)  # 用 0 填充缺失值

    # 填充整列
    summary_pivot['整体'] = summary_pivot['整体'].astype(float)
    summary_pivot['男'] = summary_pivot.get('男', 0).astype(float)
    summary_pivot['女'] = summary_pivot.get('女', 0).astype(float)

    # 按整体平均配速排序
    summary_pivot.sort_values(by='整体', ascending=True, inplace=True)

    # 绘制比较条形图
    plt.figure(figsize=(12, 6))

    # Specifying color list that matches your data
    colors = ['skyblue', 'orange', 'lightgreen']
    summary_pivot.plot(x='团队名称', kind='bar', stacked=False, color=colors)

    # 添加标题和标签
    plt.title('各大学选手配速比较（按整体平均速度排序）', fontsize=16)
    plt.xlabel('大学', fontsize=12)
    plt.ylabel('配速（秒）', fontsize=12)

    # 设置 x 轴的刻度旋转
    plt.xticks(rotation=45, fontsize=10)
    plt.legend(title='平均配速类型', fontsize=10)
    plt.grid(axis='y')

    # 显示图形
    plt.tight_layout()  # 自动调整布局
    plt.show()


# 计算每个大学的平均速度
import pandas as pd


def output_average_speed_ranked_to_md():
    # 整体平均速度
    overall_avg_speed = df.groupby('团队名称')['配速（秒）'].mean().reset_index()
    overall_avg_speed['整体'] = overall_avg_speed['配速（秒）']

    # 按性别计算平均速度
    avg_speed_gender = df.groupby(['团队名称', '性别'])['配速（秒）'].mean().reset_index()
    avg_speed_gender = avg_speed_gender.pivot(index='团队名称', columns='性别', values='配速（秒）').reset_index()
    avg_speed_gender.columns.name = None  # 去掉列索引名称

    # 合并数据
    summary = pd.merge(overall_avg_speed, avg_speed_gender, on='团队名称')
    # print(summary)
    print(summary.columns)


    # 排名
    summary['排名'] = summary['整体'].rank(ascending=True, method='min').astype(int)  # 直接按整体排名
    summary['女子排名'] = summary['女'].rank(ascending=True, method='min').astype(int)
    summary['男子排名'] = summary['男'].rank(ascending=True, method='min').astype(int)
    # 输出结果并按排名排序

    summary['配速（秒）'] = summary['配速（秒）'].apply(seconds_to_pace)
    summary['男'] = summary['男'].apply(seconds_to_pace)
    summary['女'] = summary['女'].apply(seconds_to_pace)
    summary['整体'] = summary['整体'].apply(seconds_to_pace)
    summary['排名'] = summary['排名'].astype(int)
    ranked_summary = summary.sort_values(by=['整体'])
    ranked_summary = ranked_summary.sort_values(by=['整体'])
    # 创建 Markdown 文件
    with open('average_speed_ranked.md', 'w', encoding='utf-8') as f:
        f.write("# 各大学的平均速度排名\n\n")
        f.write("| 团队名称 | 配速（秒） | 男 | 女 | 整体 | 排名 | 女子排名 | 男子排名 |\n")
        f.write("| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |\n")

        # 写入每一行数据
        for index, row in ranked_summary.iterrows():
            f.write(
                f"| {row['团队名称']} | {row['配速（秒）']} | {row.get('男', '')} | {row.get('女', '')} | {row.get('整体', '')} | {int(row['排名'])} | {int(row['女子排名'])} | {int(row['男子排名'])} |\n")


# 调用函数
# output_average_speed_ranked_to_md()


def ave_alternative():
    # 计算整体平均配速
    overall_avg_pace = df.groupby('团队名称')['配速（秒）'].mean().reset_index()
    overall_avg_pace['性别'] = '整体'

    # 计算按性别分开的平均配速
    avg_pace_gender = df.groupby(['团队名称', '性别'])['配速（秒）'].mean().reset_index()

    # 整合数据
    summary = pd.concat([overall_avg_pace, avg_pace_gender])

    # 将数据重塑为大学为行，平均配速为列
    summary_pivot = summary.pivot(index='团队名称', columns='性别', values='配速（秒）').reset_index()

    # 填充 NaN 值
    summary_pivot.fillna(0, inplace=True)

    # 按整体平均配速排序
    summary_pivot.sort_values(by='整体', ascending=True, inplace=True)

    # 使用 seaborn 绘制比较条形图
    plt.figure(figsize=(12, 6))
    summary_melted = summary_pivot.melt(id_vars='团队名称', value_vars=['整体', '男', '女'],
                                        var_name='性别', value_name='配速（秒）')

    # 绘制条形图
    sns.barplot(x='团队名称', y='配速（秒）', hue='性别', data=summary_melted, palette='pastel')

    # 添加标题和标签
    plt.title('各大学选手配速比较（按整体平均速度排序）', fontsize=16)
    plt.xlabel('大学', fontsize=12)
    plt.ylabel('配速（秒）', fontsize=12)

    # 设置 x 轴的刻度旋转
    plt.xticks(rotation=45, fontsize=10)
    plt.legend(title='平均配速类型', fontsize=10)
    plt.grid(axis='y')

    # 显示图形
    plt.tight_layout()  # 自动调整布局
    plt.show()


# 调
output_average_speed_ranked_to_md()
