import pandas as pd
import numpy as np

# 读取 Markdown 文件
md_file = 'shen_yang.md'  # 你的 Markdown 文件名
data = []

with open(md_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 跳过前一行（标题），从剩下的数据中读取
for line in lines[1:]:
    if line.strip():  # 如果行不为空
        parts = line.strip().split('\t')  # 使用制表符分割
        data.append(parts)

# 生成 DataFrame，转换数据类型
df = pd.DataFrame(data, columns=['名次', '团队名称', '姓名', '性别', '编号', '圈数', '耗时'])

# 转换数值型数据
df['圈数'] = df['圈数'].astype(int)
df['耗时'] = pd.to_timedelta(df['耗时'])
df['总耗时（秒）'] = df['耗时'].dt.total_seconds()/4

# 计算每个团队的男女平均速度
results = df.groupby(['团队名称', '性别']).agg(
    平均速度=('总耗时（秒）', 'mean'),
    中位数=('总耗时（秒）', 'median'),
    方差=('总耗时（秒）', 'var')
).reset_index()

# 将平均速度转化为“分钟:秒”格式
def seconds_to_minutes_seconds(total_seconds):
    if total_seconds is None:
        return "N/A"
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:05.2f}"

# 应用转换函数
results['平均速度'] = results['平均速度'].apply(seconds_to_minutes_seconds)
results['中位数'] = results['中位数'].apply(seconds_to_minutes_seconds)

# 计算总平均速度（男女一起）
overall_results = df.groupby('团队名称').agg(
    总平均速度=('总耗时（秒）', 'mean'),
).reset_index()

# 转化为“分钟:秒”格式
overall_results['总平均速度'] = overall_results['总平均速度'].apply(seconds_to_minutes_seconds)

# 合并结果
final_results = pd.merge(results, overall_results, on='团队名称', how='outer')

# 创建女子平均速度列
# 将女子平均速度从之前的结果中提取
women_results = results[results['性别'] == '女'][['团队名称', '平均速度']].rename(columns={'平均速度': '女子平均速度'})

# 通过左连接将女子平均速度合并到最终结果
final_results = pd.merge(final_results, women_results, on='团队名称', how='left')

# 创建男子平均速度列
final_results['男子平均速度'] = final_results['平均速度'].where(final_results['性别'] == '男')

# 创建男子排名，只计算有效的男子平均速度
final_results['男子排名'] = final_results['男子平均速度'].rank(method='min', na_option='bottom')

# 创建女子排名，处理NaN值
final_results['女子排名'] = (final_results['女子平均速度'].rank(method='min', na_option='bottom')+1)/2
# print(final_results['女子平均速度'])
# 按男子平均速度排序，只保留男性行
final_results = final_results[final_results['性别'] == '男'].sort_values(by='总平均速度')

# 重新排列列的顺序
final_results = final_results[['团队名称', '男子平均速度', '中位数', '方差', '女子排名', '女子平均速度', '总平均速度', '男子排名']]

# 将方差转换为合适的格式（取绝对值或显示"N/A"）
final_results['方差'] = final_results['方差'].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "N/A")

# 创建Markdown表格
markdown_table = "| 团队名称 | 总平均速度 | 中位数 | 方差 | 女子排名 | 女子平均速度 | 男子平均速度 | 男子排名 |\n"
markdown_table += "| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |\n"

for index, row in final_results.iterrows():
    markdown_table += f"| {row['团队名称']} | {row['总平均速度']} | {row['中位数']} | {row['方差']} | {row['女子排名']} | {row['女子平均速度']} | {row['男子平均速度']} | {row['男子排名']} |\n"

# 保存Markdown文件
with open('团队统计结果.md', 'w', encoding='utf-8') as f:
    f.write(markdown_table)

print("统计结果已保存至 '团队统计结果.md'")
