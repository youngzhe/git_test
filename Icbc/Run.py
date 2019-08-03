import datetime
import subprocess

from scrapy import cmdline
from scrapy.cmdline import execute
import sys, time, os

# os.system('scrapy crawl starFinanceCrawl')
os.system('scrapy crawl privateRecommendCrawl')

# CYCLE_TIME = 30*1
# #'starFinanceCrawl', 'goldCrawl', 'exchangeRateCrawl'
# spiders = ['starFinanceCrawl']
#
# cmd = 'scrapy crawl {}'
#
# i = 0
# while True:
#     for s in spiders:
#         subprocess.Popen(cmd.format(s), shell=True if os.name == 'posix' else False)
#     i += 1
#     print("第{}轮执行".format(i))
#     if i%3==0:
#         subprocess.Popen(cmd.format('exchangeRateCrawl'), shell=True if os.name == 'posix' else False)
#     time.sleep(CYCLE_TIME)






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