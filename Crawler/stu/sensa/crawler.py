from crawlerUtil import do_crawler

if __name__ == '__main__':
    do_crawler("https://news.gmw.cn/node_4108", "//li/span/a")
    do_crawler("https://guancha.gmw.cn/node_86599", "//ul[@class='channel-newsGroup']/li/span/a")
    do_crawler("https://guancha.gmw.cn/node_102342", "//ul[@class='channel-newsGroup']/li/span/a")
    do_crawler("https://politics.gmw.cn/node_9844", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://politics.gmw.cn/node_9840", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://politics.gmw.cn/node_9842", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://politics.gmw.cn/node_9843", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://politics.gmw.cn/node_9828", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://politics.gmw.cn/node_9831", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://politics.gmw.cn/node_26858", "//ul[@class='channel-newsGroup']/li/a")

    # 经济
    do_crawler("https://economy.gmw.cn/node_59269", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://economy.gmw.cn/node_8971", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://economy.gmw.cn/node_144789", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://economy.gmw.cn/node_144788", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://economy.gmw.cn/node_12466", "//ul[@class='channel-newsGroup']/li/a")

    # 教育
    do_crawler("https://edu.gmw.cn/node_9729", "/html/body/div[6]/div[1]/div[2]/ul/li/span/a")
    do_crawler("https://edu.gmw.cn/node_9757", "/html/body/div[6]/div[1]/div[2]/ul/li/span/a")
    do_crawler("https://edu.gmw.cn/node_10602", "/html/body/div[6]/div[1]/div[2]/ul/li/span/a")

    do_crawler("https://edu.gmw.cn/node_9722", "/html/body/div[6]/div[1]/div[2]/ul/li/span/a")
    do_crawler("https://edu.gmw.cn/node_9746", "/html/body/div[6]/div[1]/div[2]/ul/li/span/a")
    do_crawler("https://edu.gmw.cn/node_10810", "/html/body/div[6]/div[1]/div[2]/ul/li/span/a")

    # 科技
    do_crawler("https://tech.gmw.cn/node_10617", "//ul[@class='channel-newsGroup']/li/span/a")
    do_crawler("https://tech.gmw.cn/node_4360", "//ul[@class='channel-newsGroup']/li/span/a")

    # 文化
    do_crawler("https://culture.gmw.cn/node_10572", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://culture.gmw.cn/node_10565", "//ul[@class='channel-newsGroup']/li/a")

    do_crawler("https://mil.gmw.cn/node_8981", "//ul[@class='channel-newsGroup']/li/a")
    do_crawler("https://e.gmw.cn/node_7512", "//ul[@class='channel-newsGroup']/li/a")
