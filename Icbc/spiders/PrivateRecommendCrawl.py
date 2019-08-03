import datetime

import scrapy

from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from Icbc.mpsitems import PrivateRecommendFinance


class PrivateRecommendCrawlSpider(scrapy.Spider):
    name = 'privateRecommendCrawl'
    allowed_domains = ['mybank.icbc.com.cn']
    # start_urls = ["https://mybank.icbc.com.cn/icbc/newperbank/perbank3/fund/frame_fund_nologin.jsp?Flag=1&pageFlag=0&menuFlag=9&Area_code=&requestChannel=302"]
    start_urls = ["https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&menuLabel=10$17$TJ&Area_code=0200&requestChannel=302"]
    pageNumbers = []
    menuFlag = 0

    def __init__(self):
        super(PrivateRecommendCrawlSpider, self).__init__(name='privateRecommendCrawl')
        option = FirefoxOptions()
        option.headless = True
        # ,executable_path=r'/home/yangzhe/tool_station/geckodriver/geckodriver'
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

        # 拼接多url
        # if self.menuFlag < 7:
        #     self.menuFlag += 1
        #     url = self.url + str(self.menuFlag)
        #     yield scrapy.Request(url, callback=self.parse)

    # 私行推荐
    def parse_next(self, response):

        itemList = response.xpath('//*[@id="datatableModel"]/div')
        if (len(itemList) > 1):
            del itemList[0]
            # print(len(itemList))
            i=0;
            updateTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for item in itemList[:-1]:

            privateRecommendFinance = PrivateRecommendFinance()

            privateRecommendFinance['item_mark'] = "privateRecommendFinance"
            # 名称//*[@id="circularcontainer_0"]/div[1]/span[1]/span[1]/a
            privateRecommendFinance['product_name']= item.xpath('/html/body/div[1]/div[1]/div[3]/div['+str(i+2)+']/div[2]/div[1]/span[1]/span[1]/a/text()').extract_first()
            # 预期年化收益率
            a = item.xpath('//*[@id="doublelabel1_'+str(i)+'-content"]/text()').extract_first()
            if "为" in a:
                c= a.split("为")[1:][0]
            else:
                c=a
            privateRecommendFinance['performance_banchmark'] = c
            # 起购金额
            privateRecommendFinance['up_purchase_amount'] = item.xpath('//*[@id="doublelabel2_'+str(i)+'-content"]/b/text()').extract_first()
            # 期限
            m=item.xpath('//*[@id="doublelabel3_'+str(i)+'-content"]/b/text()').extract_first()
            if m is not None:
                n=item.xpath('//*[@id="doublelabel3_'+str(i)+'-content"]/text()').extract_first()+m+item.xpath('//*[@id="doublelabel3_3-content"]/text()[2]').extract_first()
            else:
                n=item.xpath('//*[@id="doublelabel3_'+str(i)+'-content"]/text()').extract_first()
            privateRecommendFinance['investment_period'] =n
            # print(privateRecommendFinance['investment_period'])
            # 风险等级
            privateRecommendFinance['risk_class'] = item.xpath('//*[@id="tt'+str(i)+'-content"]/text()').extract_first()
            # 最近购买开放日
            b = item.xpath('/html/body/div[1]/div[1]/div[3]/div['+str(i+2)+']/div[2]/div[1]/span[2]/span/text()').extract_first()
            privateRecommendFinance['raising_period'] = b.split("：")[1:][0]
            # 更新日期
            privateRecommendFinance['update_time'] = updateTime
            print(privateRecommendFinance)
            i=i+1
            yield privateRecommendFinance









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







