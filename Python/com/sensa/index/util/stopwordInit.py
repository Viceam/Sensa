import redis

words = []

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# 读取停止词，写入集合中 集合键名称：stopwords
def read_words(filename):
    with open("../../../stopwordLists/" + filename, "r", encoding="utf-8") as s1:
        words_ = s1.readlines()
    for word in words_:
        words.append(word.strip("\n"))  # 去除换行符
    print(words)
    for word in words:
        conn.sadd("stopwords", word)



