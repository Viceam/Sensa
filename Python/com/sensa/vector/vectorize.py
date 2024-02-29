import redis
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re

model = SentenceTransformer('.\\data\\pretrained_model\\all-MiniLM-L6-v2')
conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# 向量维度
dimension = 384
# 创建索引
index = faiss.IndexFlatL2(dimension)


# 分句
def split_sentences(text):
    # 使用正则表达式定义分句的标点符号
    sentence_delimiters = r'[。？！；]\s*'

    # 使用正则表达式分割句子
    sentences = re.split(sentence_delimiters, text)

    # 过滤掉空句子
    sentences = [s.strip() for s in sentences if s.strip() != '']

    return sentences


# 将文章标题向量化
def vectorize():
    num = int(conn.get("news_num")) + 1
    for i in range(1, num):
        cur = "news" + str(i)
        if not conn.exists(cur):
            continue
        print("正在处理新闻" + str(i))

        title = conn.lrange(cur, 1, 1)[0]

        sentence_embeddings = model.encode([title])

        # 添加向量到 FAISS 索引
        index.add(sentence_embeddings.astype(np.float32).reshape(1, -1))

        # 记录映射 faiss_id 到新闻编号
        faiss_id = index.ntotal - 1  # FAISS ID 是从 0 开始的
        conn.hset("faissMap", "faiss" + str(faiss_id), "news" + str(i))


vectorize()

# 保存 Faiss索引到
faiss.write_index(index, ".\\sensa.index")

print("All Done.")
