import redis
import jieba
import math

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# 计算词的idf
def idf_get():
    keys = conn.keys()
    _sum = conn.get("news_num")
    for key in keys:
        if key.startswith("idx:"):
            print(key)
            idf = math.log(int(_sum) / conn.zcard(key))
            word = key[5:]
            conn.set("idf" + word, idf)

    print("ok")


if __name__ == '__main__':
    idf_get()
