import scrapy

from Icbc.items import FundInfoItem
from Icbc.items import FundPerformanceItem
from selenium import webdriver
from selenium.webdriver import FirefoxOptions



class icbcCrawlSpider(scrapy.Spider):
    name = 'icbcCrawl'
    allowed_domains = ['mybank.icbc.com.cn']
    start_urls = ["https://mybank.icbc.com.cn/icbc/newperbank/perbank3/fund/frame_fund_nologin.jsp?Flag=1&pageFlag=0&Area_code=&requestChannel=302&menuFlag=0"]
    pageNumbers = []
    next_urls = []
    url = "https://mybank.icbc.com.cn/icbc/newperbank/perbank3/fund/frame_fund_nologin.jsp?Flag=1&pageFlag=0&Area_code=&requestChannel=302&menuFlag="
    menuFlag = 0

    def __init__(self):
        super(icbcCrawlSpider, self).__init__(name='icbcCrawl')
        option = FirefoxOptions()
        option.headless = True
        self.driver = webdriver.Firefox(options=option)

    def parse(self, response):
        # 获取每种类型下的页数
        pageNumber = int(response.xpath('//*[@id="pageturn"]/ul/li[4]/span[2]/b/text()'). extract_first())
        self.pageNumbers.append(pageNumber)
        # 拼接每一页的url
        for i in range(0, len(self.pageNumbers)):
            next_urls = []
            for currNum in range(1, self.pageNumbers[i]+1):
                next_url = response.url + "&currPageNum=" + str(currNum)
                next_urls.append(next_url)
                # 爬取每页的基金列表数据
        for next_url in next_urls:
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse_next, dont_filter=True)

        # 拼接多url
        if self.menuFlag < 7:
            self.menuFlag += 1
            url = self.url + str(self.menuFlag)
            yield scrapy.Request(url, callback=self.parse)


    # 爬取每页的基金列表数据
    def parse_next(self, response):
        ItemList = response.xpath('//div[@id="datatableModel"]/table/tbody/tr')
        for item in ItemList:
            # 列表列数
            itemcount = len(item.xpath('td').getall())
            fundInfoItem = FundInfoItem()
            ftype = item.xpath('td[1]/div/text()').extract_first()
            fundname = item.xpath('td[2]/@title').extract_first()
            fundid = item.xpath('@id').extract_first()
            fundInfoItem['ftype'] = ftype
            fundInfoItem['fundid'] = fundid
            fundInfoItem['fundname'] = fundname
            fundInfoItem['itemcount'] = itemcount
            fundInfoItem['itemtype'] = "fundinfo"
            # 爬取每个基金的基本信息1
            detail2_url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/FundGeneral.aspx?PostId=" + fundInfoItem['fundid']
            # detail_url = "https://mybank.icbc.com.cn/icbc/newperbank/perbank3/fund/fund_buy_detail_nologin.jsp?Flag=4&FundNo=" + fundid +"&Area_code=0200&requestChannel=302"
            yield scrapy.Request(url=detail2_url, meta={'fundInfoItem': fundInfoItem}, callback=self.detail_parse, dont_filter=True)

    def detail_parse(self, response):
        print("fundinfoitem-----")
        fundInfoItem = response.meta['fundInfoItem']
        if fundInfoItem['itemcount'] == 8:
            fundInfoItem['fundtype'] = response.xpath('//*[@id="fundTd27"]/text()').extract_first()
            fundInfoItem['currtype'] = response.xpath('//*[@id="fundTd29"]/text()').extract_first()
            fundInfoItem['lbbaselrg'] = ""
            fundInfoItem['lbbaselsg'] = ""
            fundInfoItem['lbbasezrg'] = ""
            fundInfoItem['lbbasegrades'] = ""
        else:
            fundInfoItem['fundtype'] = response.xpath('//*[@id="fundTd3"]/text()').extract_first()
            fundInfoItem['currtype'] = ""
            fundInfoItem['lbbaselrg'] = response.xpath('//*[@id="fundTd12"]/text()').extract_first()
            fundInfoItem['lbbaselsg'] = response.xpath('//*[@id="fundTd12"]/text()').extract_first()
            fundInfoItem['lbbasezrg'] = response.xpath('//*[@id="fundTd12"]/text()').extract_first()
            fundInfoItem['lbbasegrades'] = response.xpath('//*[@id="fundTd12"]/text()').extract_first()
        # 爬取基本信息2+基金经理信息
        detail2_url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/FundGeneral.aspx?PostId="+fundInfoItem['fundid']
        yield scrapy.Request(url=detail2_url, meta={'fundInfoItem': fundInfoItem}, callback=self.detail2_parse,
                             dont_filter=True)

    def detail2_parse(self, response):
        fundInfoItem = response.meta['fundInfoItem']
        fundInfoItem['shortname'] = response.xpath('//*[@id="lbFundShortName"]/text()').extract_first()
        fundInfoItem['fundcompanyname'] = response.xpath('//*[@id="lbFundCOMPANYID"]/text()').extract_first()
        fundInfoItem['lbbasechg'] = response.xpath('//*[@id="lbFundGuiMo"]/text()').extract_first()
        fundInfoItem['lbbasecreate'] = response.xpath('//*[@id="lbFundCREATED_DATE"]/text()').extract_first()
        yield fundInfoItem
        # print("next2_url:"+response.url)
    #     # 1、基金概况
    #     fundInfoItem = response.meta['fundInfoItem']
    #     # 基金规模
    #     fundInfoItem['lbbasechg'] = response.xpath('//*[@id="lbBaseCHG"]/text()').extract_first()
    #     # 成立日期
    #     fundInfoItem['lbbasecreate'] = response.xpath('//*[@id="lbBaseCreate"]/text()').extract_first()
    #     # 首笔最低认购金额
    #     fundInfoItem['lbbaselrg'] = response.xpath('//*[@id="lbBaseLRG"]/text()').extract_first()
    #     # 最低申购金额
    #     fundInfoItem['lbbaselsg'] = response.xpath('//*[@id="lbBaseLSG"]/text()').extract_first()
    #     # 追加认购最低金额
    #     fundInfoItem['lbbasezrg'] = response.xpath('//*[@id="lbBaseZRG"]/text()').extract_first()
    #     # 投资级差金额
    #     fundInfoItem['lbbasegrades'] = response.xpath('//*[@id="lbBaseGRADES"]/text()').extract_first()
    #     # 基金公司名称
    #     fundInfoItem['fundcompanyname'] = response.xpath('//*[@id="lbBaseGLR"]/text()').extract_first()
    #     # 2、基金净值
    #     fundPerformanceItem = FundPerformanceItem()
    #     fundPerformanceItem['itemtype'] = "fundperformanceitem"
    #     # 基金ID
    #     fundPerformanceItem['fundid'] = fundInfoItem['fundid']
    #     if (fundInfoItem['fundtype'] == ""):
    #         fundInfoItem['fundtype'] = response.xpath('//*[@id="lbBaseType"]/text()').extract_first()
    #         if(fundInfoItem['fundtype'] == None or fundInfoItem['fundtype'] == ""):
    #             detail2_url ="https://mybank.icbc.com.cn/icbc/newperbank/perbank3/fund/fund_buy_detail_nologin.jsp?Flag=4&FundNo="+fundInfoItem['fundid']+"&Area_code=1900&requestChannel=302"
    #             yield scrapy.Request(url=detail2_url, meta={'fundInfoItem': fundInfoItem}, callback=self.detail2_next, dont_filter=True)
    #
    #     # 单位净值
    #     fundPerformanceItem['buyprice'] = response.xpath('//*[@id="lbNavUnit"]/text()').extract_first()
    #     # 累计净值
    #     fundPerformanceItem['sumprice'] = response.xpath('//*[@id="lbNavCom"]/text()').extract_first()
    #     # 日涨跌
    #     fundPerformanceItem['fi_nav3'] = response.xpath('//*[@id="form1"]/table[1]/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[7]/td[2]/span/text()').extract_first()
    #     # 一周回报率
    #     fundPerformanceItem['return_1week'] = response.xpath('//*[@id="lbCX6"]/text()').extract_first()
    #     # 一月回报率
    #     fundPerformanceItem['return_1month'] = response.xpath('//*[@id="lbCX9"]/text()').extract_first()
    #     # 三月回报率
    #     fundPerformanceItem['return_3month'] = response.xpath('//*[@id="lbCX11"]/text()').extract_first()
    #     # 六月回报率
    #     fundPerformanceItem['return_6month'] = response.xpath('//*[@id="lbCX13"]/text()').extract_first()
    #     # 一年回报率
    #     fundPerformanceItem['return_1year'] = response.xpath('//*[@id="lbCX14"]/text()').extract_first()
    #     # 今年回报率
    #     fundPerformanceItem['return_thisyear'] = response.xpath('//*[@id="lbCX18"]/text()').extract_first()
    #     # 两年回报率
    #     fundPerformanceItem['return_2year'] = response.xpath('//*[@id="lbCX16"]/text()').extract_first()
    #     # 成立以来回报率
    #     fundPerformanceItem['return_base'] = response.xpath('//*[@id="lbCX20"]/text()').extract_first()
    #     return fundPerformanceItem,fundInfoItem
    #
    # def detail2_next(self, response):
    #     fundInfoItem = response.meta['fundInfoItem']
    #     print(fundInfoItem)
    #     print("once again................")
    #     fundInfoItem['fundtype'] = response.xpath('//*[@id="fundTd3"]/text()').extract_first()
    #     if(fundInfoItem['fundtype'] == None or fundInfoItem['fundtype'] == ""):
    #         fundInfoItem['fundtype'] = response.xpath('//*[@id="fundTd27"]/text()').extract_first()
    #     yield fundInfoItem



