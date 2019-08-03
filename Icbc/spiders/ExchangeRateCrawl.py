import datetime

import scrapy

from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from Icbc.mpsitems import ExchangeRate


class ExchangeRateCrawlSpider(scrapy.Spider):
    name = 'exchangeRateCrawl'
    allowed_domains = ['mybank.icbc.com.cn']
    start_urls = ["http://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx"]
    # start_urls = ["https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&menuLabel=10$17$TJ&Area_code=0200&requestChannel=302"]
    pageNumbers = []
    menuFlag = 0

    def __init__(self):
        super(ExchangeRateCrawlSpider, self).__init__(name='exchangeRateCrawl')
        option = FirefoxOptions()
        option.headless = True
        self.driver = webdriver.Firefox(options=option,executable_path='/usr/local/bin/geckodriver/geckodriver')

    def parse(self, response):
        # itemList = response.xpath('//*[@id="datatableModel"]/div')
        # print(itemList)
        # 爬取明星产品信息
        # starFinance_url = "https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&Area_code=0200&requestChannel=302"
        # yield scrapy.Request(url=starFinance_url, callback=self.starFinance_parse, dont_filter=True)
        # 爬取私行推荐信息,单个页面数据时
        # privateRecommendFinance_url = "https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&menuLabel=10$17$TJ&Area_code=0200&requestChannel=302"
        # yield scrapy.Request(url=privateRecommendFinance_url, callback=self.privateRecommendFinance_parse, dont_filter=True)
        #
        exchangeRate_url = "http://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx"
        yield scrapy.Request(url=exchangeRate_url, callback=self.exchangeRate_parse, dont_filter=True)

    # 外汇牌价信息
    def exchangeRate_parse(self, response):

        itemList = response.xpath('/html/body/form/div/table/tr[1]/td/table/tr[2]/td/table/tr')
        if (len(itemList) > 1):
            del itemList[0]
        for item in itemList:
            exchangeRate = ExchangeRate()
            exchangeRate['item_mark'] = "exchangeRate"
            # 币种
            exchangeRate['currency_type'] = item.xpath('td[1]/text()').extract_first()
            # 现汇买入价
            exchangeRate['currency_buying_price'] = item.xpath('td[2]/text()').extract_first()
            # 现钞买入价
            exchangeRate['cash_buying_price'] = item.xpath('td[3]/text()').extract_first()
            # 现汇卖出价
            exchangeRate['currency_selling_price'] = item.xpath('td[4]/text()').extract_first()
            # 现钞卖出价
            exchangeRate['cash_selling_price'] = item.xpath('td[5]/text()').extract_first()
            # 发布时间
            exchangeRate['update_time'] = item.xpath('td[6]/text()').extract_first()
            # 单位：人民币/100外币
            exchangeRate['unit'] = item.xpath('/html/body/form/div/table/tr[1]/td/table/tr[1]/td/table/tr/td[2]/text()').extract_first()
            print(exchangeRate)
            yield exchangeRate









    # 爬取每页的基金列表数据
    # def parse_next(self, response):
    #     ItemList = response.xpath('//div[@id="datatableModel"]/table/tbody/tr')
    #     # print()
    #     a=0
    #     updateTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     for item in ItemList:
    #         privateRecommendFund=PrivateRecommendFund()
    #         privateRecommendFund['item_mark'] = "privateRecommendFund"
    #         privateRecommendFund['item_code'] = item.xpath('td[1]/font/text()').extract_first()
    #         privateRecommendFund['item_name'] = item.xpath('td[2]/font/text()').extract_first()
    #         privateRecommendFund['unit_net_value'] = item.xpath('td[3]/font/text()').extract_first()
    #         privateRecommendFund['total_net_value'] = item.xpath('td[4]/font/text()').extract_first()
    #         privateRecommendFund['day_risefall'] = item.xpath('td[5]/font/text()').extract_first()
    #         privateRecommendFund['month_risefall'] = item.xpath('td[6]/font/text()').extract_first()
    #         privateRecommendFund['grade'] = item.xpath('td[7]/font/text()').extract_first()
    #         privateRecommendFund['status'] = item.xpath('td[8]/font/text()').extract_first()
    #         privateRecommendFund['update_time'] = updateTime
    #         print(privateRecommendFund)
    #         a+=1
    #         yield privateRecommendFund
    #     print(a)







