import sentencepiece as spm
from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# 假设你的训练数据保存在 'data.txt' 文件中
input_file = 'data.txt'
model_prefix = 'bpe_model'
vocab_size = 8000  # 你想要的词汇表大小

# 训练 BytePiece 分词器
spm.SentencePieceTrainer.Train(
    f'--input={input_file} --model_prefix={model_prefix} --vocab_size={vocab_size} --model_type=bpe')

# 加载 BytePiece 分词器
sp = spm.SentencePieceProcessor(model_file='bpe_model.model')


# 读取和处理数据
def tokenize(text):
    # print(sp.encode(text, out_type=str))
    return sp.encode(text, out_type=str)


# 读取训练数据并进行分词
sentences = []
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        sentences.append(tokenize(line.strip()))
        # print(sentences[-1])

# 训练 Word2Vec 模型
word2vec_model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

# 获取词向量
words = list(word2vec_model.wv.index_to_key)
print(words)
word_vectors = np.array([word2vec_model.wv[word] for word in words])
print(word_vectors)
#

# 使用 t-SNE 降维
tsne = TSNE(n_components=2, random_state=0)
reduced_vectors = tsne.fit_transform(word_vectors)

# 计算数据中心
x_mean = reduced_vectors[:, 0].mean()
y_mean = reduced_vectors[:, 1].mean()

# 绘制 t-SNE 图
plt.figure(figsize=(12, 8))
plt.scatter(reduced_vectors[:, 0], reduced_vectors[:, 1], marker='o', alpha=0.1, c='b')

# 设置坐标轴范围，使数据居中
plt.xlim(x_mean - 1.5, x_mean + 1.5)
plt.ylim(y_mean - 1, y_mean + 1)

# 标注最重要的词（例如前20个）
for i, word in enumerate(words[:20]):
    plt.annotate(word, (reduced_vectors[i, 0], reduced_vectors[i, 1]), fontsize=9, alpha=0.7)

plt.title('t-SNE Visualization of Word Embeddings')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.grid(True)
plt.show()
