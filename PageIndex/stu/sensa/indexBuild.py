import redis
import jieba
import re

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

if __name__ == '__main__':
    for i in range(1, 778):
        print("正在处理新闻" + str(i))
        text = conn.lindex("news" + str(i), 2)
        words = jieba.cut_for_search(text, HMM=True)
        for word in words:
            if not conn.sismember("stopwords", word):
                if conn.sismember("indexed", word):
                    conn.zincrby("index" + word, value="news" + str(i), amount=1)
                else:
                    conn.zadd("index" + word, {"news" + str(i): 1})

    print("OK")
