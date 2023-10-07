import redis
import jieba
import math

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def idf_get():
    keys = conn.keys()
    sum = conn.get("news_num")
    for key in keys:
        if key.startswith("index") and not key.startswith("indexed"):
            print(key)
            idf = math.log(int(sum) / conn.zcard(key))
            word = key[5:]
            conn.set("idf" + word, idf)

    print("ok")


if __name__ == '__main__':
    idf_get()
