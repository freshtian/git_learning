# 导入所需库
from tokenizers import Tokenizer

# 加载训练好的分词器
tokenizer = Tokenizer.from_file('tokenizer.json')

# 测试文本
sample_text = "this is a test sentence for tokenization.。"

# 对整个文本进行编码
encoded = tokenizer.encode(sample_text)

# 显示分词结果
print("原始文本:", sample_text)
print("Encoded IDs:", encoded.ids)
print("Tokens:", encoded.tokens)

# 逐字母显示
print("\n逐字母展示分词结果:")
for char in sample_text:
    # 使用分词器对每个字符进行编码
    char_encoded = tokenizer.encode(char)
    print(f"字符: '{char}' -> Encoded IDs: {char_encoded.ids}, Tokens: {char_encoded.tokens}")

# 还可以选择编码后的 ID 进行解码
print("\n解码已编码的内容:")
decoded_text = tokenizer.decode(encoded.ids)
print("解码后的文本:", decoded_text)
# 每个字符的输出
