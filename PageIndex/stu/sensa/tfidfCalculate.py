import redis
import jieba

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def tfidf_calculate():
    return 0
