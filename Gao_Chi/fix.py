import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

# 文件路径
file_path = 'output.txt'  # 首个数据文件路径
file_path2 = 'output.txt'  # 第二个数据文件路径


# 函数以处理心率数据
def process_heart_rate_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        content = file.readlines()

    timestamp = None
    for line in content:
        if line.startswith('  timestamp:'):
            match = re.search(r'timestamp: (.+?) \(units:', line)
            if match:
                timestamp = match.group(1).strip()
        elif line.startswith('  heart_rate:'):
            match = re.search(r'heart_rate: (\d+) \(units:', line)
            if match and timestamp:
                heart_rate = int(match.group(1).strip())
                data.append((timestamp, heart_rate))
                timestamp = None

    # 将数据转换为 DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'heart_rate'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


# 处理两个数据文件
df1 = process_heart_rate_data(file_path)
df2 = process_heart_rate_data(file_path2)

# 对于第一个文件的分析
average_heart_rate = df1['heart_rate'].mean()
std_dev_heart_rate = df1['heart_rate'].std()
lower_bound = average_heart_rate - 2 * std_dev_heart_rate
upper_bound = average_heart_rate + 2 * std_dev_heart_rate
df_filtered1 = df1[(df1['heart_rate'] >= lower_bound) & (df1['heart_rate'] <= upper_bound)]

# 计算心率差异
df1['heart_rate_diff'] = df1['heart_rate'].diff().abs()
threshold = 1

# 找出显著变化
significant_changes1 = df1[df1['heart_rate_diff'] > threshold]

# 绘制第一副图
plt.figure(figsize=(15, 15))

# 第一副图：原始心率数据
plt.subplot(3, 1, 1)
plt.scatter(significant_changes1['timestamp'], significant_changes1['heart_rate'], color='red', s=5,
            label='Significant Changes')
plt.scatter(df1['timestamp'], df1['heart_rate'], s=1, color='blue', alpha=0.5)
plt.title('Original Heart Rate over Time')
plt.xlabel('Time')
plt.ylabel('Heart Rate (bpm)')
plt.xticks(rotation=45)
plt.legend()

# 第二副图：过滤后的心率数据
plt.subplot(3, 1, 2)
plt.plot(df_filtered1['timestamp'], df_filtered1['heart_rate'], color='green', alpha=1, label='Filtered Heart Rate')
plt.title('Filtered Heart Rate over Time')
plt.xlabel('Time')
plt.ylabel('Heart Rate (bpm)')
plt.xticks(rotation=45)
plt.legend()

# 处理第二个数据文件的心率差异
df2['heart_rate_diff'] = df2['heart_rate'].diff().abs()
threshold = 2
significant_changes2 = df2[df2['heart_rate_diff'] > threshold]

# 保留相差超过20秒的时间戳
filtered_timestamps = []
previous_time = None

for i in range(len(significant_changes2) - 1):
    current_time = significant_changes2['timestamp'].iloc[i]
    if previous_time is None or (current_time - previous_time).total_seconds() >= 30:
        filtered_timestamps.append(current_time)
    previous_time = current_time

filtered_timestamps.append(significant_changes2['timestamp'].iloc[-1])
filtered_timestamps.append(df2['timestamp'].iloc[-1])

# 第三副图：心率与线性拟合
plt.subplot(3, 1, 3)
plt.scatter(df2['timestamp'], df2['heart_rate'], s=1, color='blue', alpha=1, label='Original Data')

previous_end_y = None  # 记录前一个段的结束点心率

for i in range(len(filtered_timestamps) - 1):
    start_time = filtered_timestamps[i]
    end_time = filtered_timestamps[i + 1]

    # 提取在这两个时间戳之间的数据
    segment = df2[(df2['timestamp'] >= start_time) & (df2['timestamp'] <= end_time)]

    if len(segment) > 0:
        # 使用最小二乘法进行线性拟合
        x = (segment['timestamp'] - segment['timestamp'].min()).dt.total_seconds().values.reshape(-1, 1)
        y = segment['heart_rate'].values.reshape(-1, 1)

        # 计算线性回归
        A = np.hstack([x, np.ones(x.shape)])  # 添加常数项
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]  # 最小二乘法拟合

        # 生成用于绘制的 x 数据（100 个点）
        x_fit = np.linspace(x.min(), x.max(), 100)  # 生成 100 个点

        # 根据斜率和截距计算 y_fit
        y_fit = m * x_fit + c

        # 将 x_fit 转换回时间戳
        x_fit_timestamps = segment['timestamp'].min() + pd.to_timedelta(x_fit, unit='s')

        # 绘制拟合线
        plt.plot(x_fit_timestamps, y_fit, color='red', linewidth=2)

        # 画连接线
        if previous_end_y is not None:
            plt.plot([previous_end_x, x_fit_timestamps[0]], [previous_end_y, y_fit[0]], color='red', linewidth=1)

        # 更新前一个段的结束点
        previous_end_x = x_fit_timestamps[-1]
        previous_end_y = y_fit[-1]

# 添加标签和标题
plt.title('Heart Rate with Linear Fit Between Significant Changes')
plt.xlabel('Time')
plt.ylabel('Heart Rate (bpm)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
