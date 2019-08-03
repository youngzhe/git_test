
from scrapy import cmdline
from scrapy.cmdline import execute
import os

os.system('scrapy crawl goldCrawl')
os.system('scrapy crawl exchangeRateCrawl')

# if __name__=="__main__":
#     # updateTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     str1="最近购买开放日：2019-07-25";
#     str2="上期分红适用年化收益率为3.3409％";
#     str3=":";
#     str4="为";
#
#     b=str1.split("：")[1:][0]
#     print (b)
#     c=str2.split("为")[1:][0]
#     print (c)