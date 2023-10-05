import redis
import jieba

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def index_build(mode):
    for i in range(1, 778):
        print("正在处理新闻" + str(i))
        text = conn.lindex("news" + str(i), mode)
        words = jieba.cut_for_search(text, HMM=True)
        index = "title_index" if mode == 1 else "index"
        indexed = "title_indexed" if mode == 1 else "indexed"
        for word in words:
            if not conn.sismember("stopwords", word):
                if conn.sismember(indexed, word):
                    conn.zincrby(index + word, value="news" + str(i), amount=1)
                else:
                    conn.zadd(index + word, {"news" + str(i): 1})
                    conn.sadd(indexed, word)

    print("OK")


if __name__ == '__main__':
    index_build(1)
    index_build(2)
