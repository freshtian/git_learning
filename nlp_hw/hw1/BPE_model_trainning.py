# 导入必要的库
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders, normalizers

# 步骤 1: 加载数据
# 假设 data.txt 文件在当前工作目录下
with open('data.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()

# 创建一个文本列表用于训练
texts = [line.strip() for line in data if line.strip()]

# 步骤 2: 创建和训练分词器
# 使用 BPE 模型
tokenizer = Tokenizer(models.BPE())

# 设置预处理器 (可以选择其他选项)
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()

# 创建训练器并设置词表大小
trainer = trainers.BpeTrainer(vocab_size=6000, min_frequency=2)

# 训练分词器
tokenizer.train_from_iterator(texts, trainer)

# 选项: 设置解码器和归一化器 (可选)
tokenizer.decoder = decoders.ByteLevel()
tokenizer.normalizer = normalizers.NFKC()

# 步骤 3: 保存模型
tokenizer.save('tokenizer.json')

print("分词器训练完毕，模型已保存为 tokenizer.json 文件。")
