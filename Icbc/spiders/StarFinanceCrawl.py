import datetime

import scrapy


from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from Icbc.mpsitems import StarFinance


class StarFinanceCrawlSpider(scrapy.Spider):
    name = 'starFinanceCrawl'
    allowed_domains = ['mybank.icbc.com.cn']
    start_urls = ["https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&Area_code=0200&requestChannel=302"]
    pageNumbers = []
    menuFlag = 0

    def __init__(self):
        super(StarFinanceCrawlSpider, self).__init__(name='starFinanceCrawl')
        option = FirefoxOptions()
        option.headless = True
        self.driver = webdriver.Firefox(options=option,executable_path='/usr/local/bin/geckodriver/geckodriver')

    def parse(self, response):
        # 获取每种类型下的页数
        # pageNumber = int(response.xpath('//*[@id="pageturn"]/ul/li[4]/span[2]/b/text()'). extract_first())
        pageNumber=int(response.xpath('//*[@id="pageturn"]/ul/li[3]/span[2]/b/text()').extract_first())
        print(pageNumber)
        self.pageNumbers.append(pageNumber)
        # 拼接每一页的url
        #分页的拼接字段大部分为&currPageNum=
        for i in range(0, len(self.pageNumbers)):
            next_urls = []
            for currNum in range(1, self.pageNumbers[i]+1):
                next_url = response.url + "&nowPageNum_turn=" + str(currNum)
                next_urls.append(next_url)
                # 爬取每页的基金列表数据
        for next_url in next_urls:
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse_next, dont_filter=True)



    # def __init__(self):
    #     super(StarFinanceCrawlSpider, self).__init__(name='starFinanceCrawl')
    #     option = FirefoxOptions()
    #     option.headless = True
    #     self.driver = webdriver.Firefox(options=option,executable_path='/usr/local/bin/geckodriver/geckodriver')
    #
    # def parse(self, response):
    #         # itemList = response.xpath('//*[@id="datatableModel"]/div')
    #         # print(itemList)
    #         # 爬取明星产品信息
    #         starFinance_url = "https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&Area_code=0200&requestChannel=302"
    #         yield scrapy.Request(url=starFinance_url, callback=self.starFinance_parse, dont_filter=True)
    #         # 爬取私行推荐信息,单个页面数据时
    #         # privateRecommendFinance_url = "https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&menuLabel=10$17$TJ&Area_code=0200&requestChannel=302"
    #         # yield scrapy.Request(url=privateRecommendFinance_url, callback=self.privateRecommendFinance_parse, dont_filter=True)
    #         #
    #         exchangeRate_url = "http://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx"
    #         yield scrapy.Request(url=exchangeRate_url, callback=self.exchangeRate_parse, dont_filter=True)

    # 明星产品 推荐产品
    def parse_next(self, response):

        itemList = response.xpath('//*[@id="datatableModel"]/div')
        if (len(itemList) > 1):
            del itemList[0]
            i=0;
            updateTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for item in itemList[:-1]:
            starFinance = StarFinance()

            starFinance['item_mark'] = "starFinance"
            # 产品名称
            starFinance['product_name'] = item.xpath('/html/body/div[1]/div[1]/div[3]/div['+str(i+2)+']/div[2]/div[1]/span[1]/span[1]/a/text()').extract_first()
            # 业绩比较基准
            starFinance['performance_banchmark'] = item.xpath('//*[@id="doublelabel1_'+str(i)+'-content"]/text()').extract_first()
            # 起购金额
            starFinance['up_purchase_amount'] = item.xpath('//*[@id="doublelabel2_'+str(i)+'-content"]/b/text()').extract_first()
            # 投资期限
            # item.xpath('//*[@id="doublelabel3_'+str(i)+'-content"]/b/text()').extract_first()
            m=item.xpath('//*[@id="doublelabel3_'+str(i)+'-content"]/b/text()').extract_first()
            if m is not None:
                l=item.xpath('//*[@id="doublelabel3_'+str(i)+'-content"]/text()[2]').extract_first()
                n=item.xpath('//*[@id="doublelabel3_'+str(i)+'-content"]/text()').extract_first()+m+l
            else:
                n=item.xpath('//*[@id="doublelabel3_'+str(i)+'-content"]/text()').extract_first()
            starFinance['invesment_period'] = n
            # 产品风险等级
            starFinance['risk_class'] = item.xpath('//*[@id="tt'+str(i)+'-content"]/text()').extract_first()
            # 募集期/最近购买开放日
            starFinance['raising_period'] = item.xpath('/html/body/div[1]/div[1]/div[3]/div['+str(i+2)+']/div[2]/div[1]/span[2]/span/text()').extract_first()
            # 更新日期
            starFinance['update_time'] = updateTime
            print(starFinance)
            i=i+1
            yield starFinance


