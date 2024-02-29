from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import redis
import numpy as np

app = Flask(__name__)

model = SentenceTransformer(r"../vector/data/pretrained_model/text2vec-base-chinese")
index = faiss.read_index(r"./faiss.index")
conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# 这是一个微服务 由于java并不能直接使用faiss索引，采用java客户端-python服务器的方式
# 接收 query搜索语句 k检索的新闻数量
@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data['query']
    k = data.get('k', 30)

    # 对查询进行向量化
    query_embedding = model.encode([query])

    # 执行搜索
    D, I = index.search(query_embedding.astype(np.float32).reshape(1, -1), k)

    # 获取faiss{id}到news{id}的映射
    results = []
    for idx, dist in zip(I[0], D[0]):
        faiss_id = "faiss" + str(idx)
        # 从Redis中获取对应的news{id}
        news_id = conn.hget("faissMap", faiss_id)
        if news_id:
            results.append({'index': news_id, 'distance': float(dist)})
        else:
            # 如果在Redis中找不到映射，可能需要处理错误或跳过
            print(f"Mapping for {faiss_id} not found in Redis.")

    # 返回 top-k 结果及其距离
    return jsonify(results)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
