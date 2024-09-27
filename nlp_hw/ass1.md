# Q1 [30 points]:
  从NLP领域选择三个方向，每个方向选择一个benchmark dataset。
简单介绍其输入、输出、评估方
法，并列出在该benchmark dataset上表现最佳的前两个模型/方法，简单介绍该模型/方法以及其表
现。

## 1. 文本分类
### 基准数据集：
AG News

### 输入：
新闻文章的文本内容。


### 输出：
四个类别之一（例如：
World, Sports, Business, Science/Technology）。


### 评估方法：
使用准确率（Accuracy）、宏平均F1分数（Macro F1 Score）等指标评估模型性能。


### 表现最佳的模型/方法：


BERT（Bidirectional Encoder Representations from Transformers）

BERT 是一种预训练的语言表示模型，通过双向训练来学习词汇的上下文关系。
它在多种NLP任务上表现出色。

BERT 在 AG News 上取得了非常高的准确率，因其对上下文的理解能力强大。

RoBERTa（A Robustly Optimized BERT Pretraining Approach）

RoBERTa 是 BERT 的一个优化版本，通过改进的预训练方法和增加的训练数据，进一步提升了性能。

相较于 BERT，RoBERTa 在 AG News 上展示了更优的性能，特别是在文本分类任务上。

## 2. 情感分析
### 基准数据集：
IMDb

### 输入：
电影评论的文本（正面或负面）。


### 输出：
情感极性（Positive 或 Negative）。


### 评估方法：
采用准确率（Accuracy）、精确率（Precision）、召回率（Recall）和F1分数（F1 Score）来评估模型。


### 表现最佳的模型/方法：


**DistilBERT**

DistilBERT 是 BERT 的轻量级版本，使其在保持性能的同时提高了推理速度和效率。

在 IMDb 数据集上，DistilBERT 展示了优越的情感分类能力，且推理速度更快。

XLNet

XLNet 是一种自回归模型，结合了BERT和Transformer-XL的优点，能够更好地捕获句子中的依赖关系。

在 IMDb 数据集上表现良好，XLNet 能够处理长文本并提供更准确的情感分类。

## 3. 机器翻译
### 基准数据集：
WMT (Workshop on Machine Translation)

### 输入：
一段文本（源语言，如英语）。


### 输出：
翻译后的文本（目标语言，如法语）。


### 评估方法：
使用 BLEU（Bilingual Evaluation Understudy）分数来评估翻译的质量，越高越好。


### 表现最佳的模型/方法：


方向展示了 NLP 中的文本分类、情感分析和机器翻译领域，分别介绍了对应的基准数据集、输入、输出和评估方法，以及当前表现最佳的模型和其性能表现。
通过这些信息，可以更好地理解 NLP 中的最新进展和技术应用。

# Q2
请你自行搜索并学习以上算法（BPE、BBPE、Unigram、WordPiece、SentencePiece），然后从它们
的原理、计算方法、优化目标等方面展开介绍。

注意一：你不需要列举出所有关于算法的细节，我们的评分标准在于你的介绍是否全面且准确
注意二：你可能会对这些算法之间的关系感到困惑。
他们之间的关系并不是完全平行的，例如
WordPiece与BPE的原理十分相似，而SentencePiece采用BPE和Unigram作为训练算法

## BPE
BPE（Byte Pair Encoding）

**原理与计算方法**：

初始化：将训练语料中的所有字符视为初始词汇表。
可以是每个字符或字母，甚至是整个词。

统计频率：
在训练数据中统计每个字符的出现频率。

统计每对相邻字符的出现频率，生成一个字符对频率表。

合并操作：
找出频率最高的字符对（例如，'a' 和 'b' 组合成 'ab'）。

将该字符对合并为一个新符号，并将新符号添加到词汇表中。

重复合并：
重新遍历训练语料，在新符号的基础上再次统计字符对的频率。

重复以上统计和合并步骤，直到达到预定义的词汇表大小（例如，限为 10,000 个子词）或再没有可以合并的字符对。

子词生成：
通过以上步骤生成的符号构成词汇表，后续文本处理时可以使用这些子词代替原始文本，从而实现更好的分词效果。


**优化目标**： BPE 的优化目标是最大限度地减小模型在处理未登录词（out-of-vocabulary words）时的困境，同时在保证编码效率的前提下，尽可能保留语言的语义信息。


## BBPE
BBPE（Byte-Level BPE）

**原理与计算方法**：

初始化：将输入文本按照字节进行分割，而非字符。
例如，Unicode 字符串被转换为其对应的字节形式。

统计频率：
统计每个字节的频率。

统计字节对的频率，生成字节对频率表。

合并操作：
找出最常见的字节对（如 'ab'），并将其合并为一个新字节（如 'ab'）。

将新字节添加到词汇表。

重复合并：
继续统计和合并字节对，直至达到指定的词汇表大小或没有更多的字节可合并。

处理多样化文本：
考虑到不同语言的特殊字符，BBPE 可以有效处理多种语言和编码。


**优化目标**： BBPE 的目标同样是减少未登录词问题，并提高对不同语言和编码格式的适应性。

## Unigram
Unigram Language Model

**原理与计算方法**：

词汇表构建：首先，基于训练文本统计所有单词的出现次数，构建词汇表。

计算概率：
对于每个单词，计算其出现的概率：。

基于独立性假设：
假设每个词是独立选择的，给定一个句子 ，可以计算句子的生成概率为：。


**优化目标**：
通过最大化训练数据的似然函数，优化单词的选择，从而提高模型的表现。

## Unigram
WordPiece

**原理与计算方法**：

初始化：和 BPE 类似，初始化词汇表中每个字符（或符号）。

统计频率：
统计字符或子词的频率。

计算子词组合的概率，目标是找到合并后能够最大化训练语料的概率的子词组合。

合并操作：
利用最大似然估计，选择那些在当前模型下能提高概率的字符对进行合并。

选择合并后对模型表现影响最大的组合，逐步构建更复杂的子词。


**优化目标**：
比较 BPE，WordPiece 主要目标是最大化在给定上下文下的似然函数，使得生成的子词对齐更有效。


## WordPiece
SentencePiece

**原理与计算方法**：

数据预处理：
对输入数据进行文本标准化，包括去除标点、分句等处理。

子词训练：
使用无监督的方法，将整个输入文本视为一串字符，构建词汇表。
可以选择用 BPE 或 Unigram 中的任意一种或两者结合。

合并和分割：
通过 BPE 操作逐渐合并字符到子词，而 Unigram 模型则根据每个子词的概率进行选择。

每一轮的合并操作后，调整概率分布，以使得使用的子词组合能更好地表示原始序列。


**优化目标**：
目标是使用最少的符号表示最多的信息，提高压缩比和处理多种语言的能力，特别是在处理未登录词时非常有效。