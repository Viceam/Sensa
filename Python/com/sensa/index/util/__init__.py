from stopwordInit import read_words

# 运行 写入停止词到集合中
if __name__ == '__main__':
    read_words("baidu_stopwords.txt")
    read_words("cn_stopwords.txt")
    read_words("hit_stopwords.txt")
    read_words("scu_stopwords.txt")
    read_words("stopwords5.txt")