import redis

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# 将TF(词频)与IDF(逆文本频率)相乘 获得完整的反向索引
def multiple():
    keys = conn.keys("idx:*")
    for key in keys:
        word = key[4:]
        # print(word)
        idf = conn.get("idf:" + word)
        if idf:
            idf = float(idf)
            # 获取该单词对应的所有文档及其词频(TF)
            doc_keys = conn.zrange(key, 0, -1, withscores=True)
            for doc_key, tf in doc_keys:
                # 计算TF-IDF得分
                tf_idf_score = tf * idf
                # 更新文档在idx:{word}中的zscore为TF-IDF得分
                conn.zadd(key, {doc_key: tf_idf_score})
    print("Done")


multiple()
