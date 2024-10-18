import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
# 文件路径
file_path = 'output.txt'

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
        if match and timestamp:  # 因为heart_rate可能为空，所以要判断一下
            heart_rate = int(match.group(1).strip())
            data.append((timestamp, heart_rate))
            timestamp = None

df = pd.DataFrame(data, columns=['timestamp', 'heart_rate'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.to_csv('heart_rate_data.txt', sep='\t', index=False)

average_heart_rate = df['heart_rate'].mean()
std_dev_heart_rate = df['heart_rate'].std()
lower_bound = average_heart_rate - 2 * std_dev_heart_rate
upper_bound = average_heart_rate + 2 * std_dev_heart_rate
df_filtered = df[(df['heart_rate'] >= lower_bound) & (df['heart_rate'] <= upper_bound)]

# 假设之前的代码已经完成，生成了 df 和 significant_changes

# 计算心率差异
df['heart_rate_diff'] = df['heart_rate'].diff().abs()
threshold = 2
significant_changes = df[df['heart_rate_diff'] > threshold]
print(significant_changes)
# 保留相差超过20秒的时间戳
filtered_timestamps = []
previous_time = None

for i in range(len(significant_changes) - 1):
    current_time = significant_changes['timestamp'].iloc[i]

    if previous_time is None or (current_time - previous_time).total_seconds() >=30:
        filtered_timestamps.append(current_time)
        print(current_time)

    previous_time = current_time

# 添加最后一个时间戳
filtered_timestamps.append(significant_changes['timestamp'].iloc[-1])
filtered_timestamps.append(df['timestamp'].iloc[-1])
# 输出保留的时间戳
print(filtered_timestamps)

# 对于每对相邻时间戳，进行最小二乘法拟合
plt.figure(figsize=(15, 10))
plt.scatter(df['timestamp'], df['heart_rate'], s=1, color='blue', alpha=1, label='Original Data')

for i in range(len(filtered_timestamps) - 1):
    start_time = filtered_timestamps[i]
    end_time = filtered_timestamps[i + 1]

    # 提取在这两个时间戳之间的数据
    segment = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

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

# 添加标签和标题
plt.title('Heart Rate with Linear Fit Between Significant Changes')
plt.xlabel('Time')
plt.ylabel('Heart Rate (bpm)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
