import redis
import jieba

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
stopwords = set(conn.smembers("stopwords"))


def idx_build():
    total = int(conn.get("news_num")) + 1
    # 对所有的新闻
    for num in range(7322, total):
        print("now:" + str(num))
        txt = conn.lrange("news" + str(num), 2, 2)[0]
        if not txt:
            print(f"No text found for news{num}.")
            continue

        words = jieba.cut_for_search(txt, HMM=True)

        filtered_words = [word for word in words if word not in stopwords]

        # 现在 filtered_words 包含了去除停止词之后的词语列表
        # 这里是保存后的结果
        words = filtered_words

        # 为词建立反向索引 使用zset存储 键名为 idx:{词} 存储的结构为{新闻编号}:{词频}
        for word in words:
            if conn.exists("idx:" + word):
                conn.zincrby("idx:" + word, amount=1.0, value="news" + str(num))
            else:
                conn.zadd("idx:" + word, {"news" + str(num): 1.0})


idx_build()
