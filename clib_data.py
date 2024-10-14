import pandas as pd
import matplotlib.pyplot as plt
import re

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

average_heart_rate = df['heart_rate'].mean()
std_dev_heart_rate = df['heart_rate'].std()
lower_bound = average_heart_rate - 2 * std_dev_heart_rate
upper_bound = average_heart_rate + 2 * std_dev_heart_rate
df_filtered = df[(df['heart_rate'] >= lower_bound) & (df['heart_rate'] <= upper_bound)]

df['heart_rate_diff'] = df['heart_rate'].diff().abs()
print(df['heart_rate_diff'].describe())

threshold = 1

significant_changes = df[df['heart_rate_diff'] > threshold]
print(significant_changes)
plt.figure(figsize=(15, 10))

plt.subplot(2, 1, 1)

plt.scatter(significant_changes['timestamp'], significant_changes['heart_rate'], color='red', s=5,
            label='Significant Changes')  # 用红色散点标记
plt.scatter(df['timestamp'], df['heart_rate'], s=1, color='blue', alpha=0.5)
plt.title('Original Heart Rate over Time')
plt.xlabel('Time')
plt.ylabel('Heart Rate (bpm)')
plt.xticks(rotation=45)

plt.subplot(2, 1, 2)
plt.plot(df_filtered['timestamp'], df_filtered['heart_rate'], color='green', alpha=1, label='Filtered Heart Rate')
plt.title('Filtered Heart Rate over Time with Significant Changes Highlighted')
plt.xlabel('Time')
plt.ylabel('Heart Rate (bpm)')
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.show()
