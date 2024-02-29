import math
import redis

# 假设这里已经建立了到Redis的连接
conn = redis.StrictRedis(host='localhost', port=6379, db=0)


def idf_get():
    _sum = int(conn.get("news_num"))
    cursor = '0'
    while True:
        cursor, keys = conn.scan(cursor=cursor, match="idx:*", count=1000)
        print(f"Cursor: {cursor}")  # 打印当前游标值
        for key in keys:
            word = key.decode('utf-8')[4:]  # 假设键是字节字符串，需要解码
            doc_count = conn.zcard(key)
            if doc_count > 0:  # 检查以避免除以零
                idf = math.log(_sum / doc_count)
                conn.set("idf:" + word, idf)
        if cursor == 0:  # 如果游标返回0，表示迭代结束
            break

    print("ok")


idf_get()
