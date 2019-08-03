import scrapy

from Icbc.items import FundRateItem
from selenium import webdriver
from selenium.webdriver import FirefoxOptions



class rateCrawlSpider(scrapy.Spider):
    name = 'rateCrawl'
    allowed_domains = ['mybank.icbc.com.cn']
    start_urls = []
    length = 0
    url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/fundratelist.aspx?PostId="
    start_urls.append(url)

    def __init__(self):
        super(rateCrawlSpider, self).__init__(name='rateCrawl')
        option = FirefoxOptions()
        option.headless = True
        self.driver = webdriver.Firefox(options=option)

    def parse(self, response):
      itemList = response.xpath('//*[@id="stID"]/option')
      url = response.url

      for item in itemList:
          fundid = item.xpath("@value").get()
          next_url = url+fundid
          yield scrapy.Request(next_url, callback=self.next_parse, dont_filter=True)

    def next_parse(self, response):

        fundid = response.xpath('//*[@id="stID"]/option[@selected="selected"]/@value').get()
        itemList = response.xpath('//*[@id="gvFund"]/tr')
        # print(len(itemList))
        # 删除表格title
        if(len(itemList) > 1):
            del itemList[0]
        # print(len(itemList))
        self.length = self.length + len(itemList)
        print(self.length)
        for item in itemList:
            fundRateItem = FundRateItem()
            fundRateItem['itemtype'] = "fundrate"
            # 费率
            fundRateItem['frate'] = item.xpath('td[2]/span/text()').get()
            # 费率类型
            fundRateItem['ratetype'] = item.xpath('td[3]/span/text()').get()
            # 费率金额
            fundRateItem['ratemoney'] = item.xpath('td[4]/span/text()').get()
            # 持有期限
            fundRateItem['funddate'] = item.xpath('td[5]/span/text()').get()
            # 基金ID
            fundRateItem['fundid'] = fundid
            yield fundRateItem


