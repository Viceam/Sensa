import redis
from selenium import webdriver
from selenium.webdriver.common.by import By
import queue
import jieba

driver = webdriver.Chrome();
conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_content(news_url, news_id):
    driver.get(news_url)
    contents = driver.find_elements(By.XPATH, "//div[@class='u-mainText']/p")
    news_content = ""
    for content in contents:
        news_content += content.text
    conn.rpush("news" + str(news_id), news_content)

if __name__ == '__main__':

    if conn.get("news_num") is None:
        conn.set("news_num", 0)

    for i in range(1, 11):
        url = "https://news.gmw.cn/node_4108"
        if i != 1:
            url = url + "_" + str(i)
        url += ".htm"

        driver.get(url)
        urls = driver.find_elements(By.XPATH, "//li/span/a")
        news_urls = []
        #解决 stale element
        q = queue.Queue()
        for ur in urls:
            news_urls.append(ur.get_attribute('href'))
            q.put(ur.text)
        for news_url in news_urls:
            print(news_url)
            if conn.sadd("news_urls", news_url) == 0:
                continue
            news_title = q.get()
            conn.incr("news_num")
            news_id = conn.get("news_num")
            conn.rpush("news" + str(news_id), news_url, news_title)
            get_content(news_url, news_id)

    driver.quit()



