import redis
from selenium import webdriver
from selenium.webdriver.common.by import By
import queue


driver = webdriver.Chrome()
conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def get_content(news_url, news_id):
    driver.get(news_url)
    contents = driver.find_elements(By.XPATH, "//div[@class='u-mainText']/p")
    news_content = ""
    for content in contents:
        news_content += content.text
    conn.rpush("news" + str(news_id), news_content)


def do_crawler(start_url, _xpath):
    for i in range(1, 11):
        url = start_url
        if i != 1:
            url = url + "_" + str(i)
        url += ".htm"
        print(url)
        driver.get(url)
        elements = driver.find_elements(By.XPATH, _xpath)
        # 解决 stale element
        news_urls = []
        q = queue.Queue()
        for element in elements:
            news_urls.append(element.get_attribute('href'))
            q.put(element.text)

        for news_url in news_urls:
            if conn.sadd("news_urls", news_url) == 0:
                continue
            news_title = q.get()
            conn.incr("news_num")
            news_id = conn.get("news_num")
            conn.rpush("news" + str(news_id), news_url, news_title)
            get_content(news_url, news_id)

