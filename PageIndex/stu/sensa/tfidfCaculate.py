import redis
import jieba

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def tfidfCaculate():
    return 0