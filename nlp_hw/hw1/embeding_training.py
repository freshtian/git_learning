import random
import numpy as np
import gensim
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from tokenizers import Tokenizer

# 1. 加载分词模型
tokenizer = Tokenizer.from_file('tokenizer.json')

# 准备你的文本数据
corpus = [
    "This is a sample sentence for word embedding.",
    "Word embedding models are very useful.",
    "Gensim makes it easy to implement.",
    "Skip-gram and CBOW are popular algorithms.",
    "Visualization is important for understanding."
]

# 2. 使用分词器对文本数据进行分词
sentences = [tokenizer.encode(sentence).tokens for sentence in corpus]

# 3. 训练 Word2Vec 模型（使用 Skip-gram）
model = gensim.models.Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=1)

# 4. 获取词嵌入
words = list(model.wv.index_to_key)
print("词汇表大小:", len(words))

# 动态选择样本数量
sample_size = min(100, len(words))
random_words = random.sample(words, sample_size)

# 5. 获取对应词的嵌入向量并转换为 NumPy 数组
word_vectors = np.array([model.wv[word] for word in random_words])

# 6. 使用 t-SNE 进行降维
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(word_vectors)

# 7. 可视化结果
plt.figure(figsize=(12, 8))
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], marker='o')

# 添加标注
for i, word in enumerate(random_words):
    plt.annotate(word, (X_tsne[i, 0], X_tsne[i, 1]))

plt.title("t-SNE visualization of Word Embeddings")
plt.xlabel("t-SNE component 1")
plt.ylabel("t-SNE component 2")
plt.grid()
plt.show()
