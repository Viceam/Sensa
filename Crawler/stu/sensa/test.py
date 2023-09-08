import redis
from selenium import webdriver
from selenium.webdriver.common.by import By
import jieba

# driver = webdriver.Chrome()
conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_content(news_url):
    # driver.get(news_url)
    # contents = driver.find_elements(By.XPATH, "//div[@class='u-mainText']/p")
    # news_content = ""
    # for content in contents:
    #     news_content += content.text
    # print(news_content)
    # conn.rpush("news" + str(conn.get("news_num")), content.text)
    return 0

if __name__ == '__main__':

    # get_content("https://news.gmw.cn/2023-09/08/content_36817829.htm")
    for i in range(1, 501):
        print(str(i))
        print(conn.lrange("news" + str(i), 0, -1))
    # driver.quit()



