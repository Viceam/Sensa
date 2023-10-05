import redis

words = []

conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# 读取停止词，写入集合中
def read_words(filename):
    with open("../../../stopwordLists/" + filename, "r", encoding="utf-8") as s1:
        words_ = s1.readlines()
    for word in words_:
        words.append(word.strip("\n"))  # 去除换行符
    print(words)
    for word in words:
        conn.sadd("stopwords", word)


if __name__ == '__main__':
    read_words("baidu_stopwords.txt")
    read_words("cn_stopwords.txt")
    read_words("hit_stopwords.txt")
    read_words("scu_stopwords.txt")
    read_words("stopwords5.txt")
