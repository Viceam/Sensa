from crawlerUtil import do_crawler

if __name__ == '__main__':
    do_crawler("https://news.gmw.cn/node_4108", "//li/span/a")
    do_crawler("https://guancha.gmw.cn/node_86599", "//ul[@class='channel-newsGroup']/li/span/a")
    do_crawler("https://guancha.gmw.cn/node_102342", "//ul[@class='channel-newsGroup']/li/span/a")






