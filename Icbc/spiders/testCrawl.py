import scrapy

from Icbc.items import FundInfoItem
from Icbc.items import FundManagerItem
from Icbc.items import CurrFundRelItem
from Icbc.items import FundPerformanceItem
from Icbc.items import FundAssetItem
from Icbc.items import ServedFundRelItem
from Icbc.items import FundAInvestItem
from Icbc.items import FundStockItem
from Icbc.items import FundBondItem
from Icbc.items import FundCompanyItem
from selenium import webdriver
from selenium.webdriver import FirefoxOptions



class testCrawlSpider(scrapy.Spider):
    name = 'testCrawl'
    allowed_domains = ['mybank.icbc.com.cn']
    start_urls = ["https://mybank.icbc.com.cn/icbc/newperbank/perbank3/fund/frame_fund_nologin.jsp?Flag=1&pageFlag=0&Area_code=&requestChannel=302&menuFlag=0"]
    pageNumbers = []
    next_urls = []
    url = "https://mybank.icbc.com.cn/icbc/newperbank/perbank3/fund/frame_fund_nologin.jsp?Flag=1&pageFlag=0&Area_code=&requestChannel=302&menuFlag="
    menuFlag = 0

    def __init__(self):
        super(testCrawlSpider, self).__init__(name='testCrawl')
        option = FirefoxOptions()
        option.headless = True
        self.driver = webdriver.Firefox(options=option,executable_path=r'/home/yangzhe/tool_station/geckodriver/geckodriver')

    def parse(self, response):
        # 获取每种类型下的页数
        pageNumber = int(response.xpath('//*[@id="pageturn"]/ul/li[4]/span[2]/b/text()').extract_first())
        self.pageNumbers.append(pageNumber)
        # 拼接每一页的url
        for i in range(0, len(self.pageNumbers)):
            next_urls = []
            for currNum in range(1, self.pageNumbers[i] + 1):
                next_url = response.url + "&currPageNum=" + str(currNum)
                next_urls.append(next_url)
                # 爬取每页的基金列表数据
        for next_url in next_urls:
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

            # 基金的基本信息1
            fundInfoItem = FundInfoItem()
            ftype = item.xpath('td[1]/div/text()').extract_first()
            fundname = item.xpath('td[2]/@title').extract_first()
            fundid = item.xpath('@id').extract_first()
            fundInfoItem['ftype'] = ftype
            fundInfoItem['fundid'] = fundid
            fundInfoItem['fundname'] = fundname
            fundInfoItem['itemcount'] = itemcount
            fundInfoItem['itemtype'] = "fundinfo"

            # 基金净值信息
            fundPerformanceItem = FundPerformanceItem()
            fundPerformanceItem['fundid'] = fundid
            # 单位净值
            fundPerformanceItem['buyprice'] = item.xpath('td[3]/font/text()').extract_first()
            # 累计净值
            fundPerformanceItem['sumprice'] = item.xpath('td[4]/a/font/text()').extract_first()
            # 日涨跌
            if itemcount == 8:
                fundPerformanceItem['fi_nav3'] = ""
            else:
                fundPerformanceItem['fi_nav3'] = item.xpath('td[5]/span/font/text()').extract_first()

            # 爬取每个基金的基本信息1
            detail_url = "https://mybank.icbc.com.cn/icbc/newperbank/perbank3/fund/fund_buy_detail_nologin.jsp?Flag=4&FundNo=" + fundid +"&Area_code=0200&requestChannel=302"
            yield scrapy.Request(url=detail_url, meta={'fundInfoItem': fundInfoItem}, callback=self.detail_parse,
                                 dont_filter=True)
            # 爬取基金净值信息
            perfor_url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/FundChenXin.aspx?PostId=" + fundid
            yield scrapy.Request(url=perfor_url, meta={'fundPerformanceItem': fundPerformanceItem}, callback=self.pefor_parse, dont_filter=True)

            # 行业投资信息
            fundAInvestItem = FundAInvestItem()
            # 基金ID
            fundAInvestItem['fundid'] = fundid
            ainvest_url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/fundInvest.aspx?PostId=" + fundid
            yield scrapy.Request(url=ainvest_url, meta={'fundAInvestItem': fundAInvestItem}, callback=self.invest_parse,
                                 dont_filter=True)
            fundAssetItem = FundAssetItem()
            fundAssetItem['fundid'] = fundid
            # 爬取资产配置信息
            asset_url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/FundAsset.aspx?PostId=" + fundid
            yield scrapy.Request(url=asset_url, meta={'fundAssetItem': fundAssetItem}, callback=self.asset_parse,
                                 dont_filter=True)
            # 基金持股明细
            fundStockItem = FundStockItem()
            fundStockItem['fundid'] = fundid
            stock_url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/FundHoldStock.aspx?PostId=" + fundid
            yield scrapy.Request(url=stock_url, meta={'fundStockItem': fundStockItem}, callback=self.stock_parse,
                                 dont_filter=True)
            # 基金持债明细
            fundBondItem = FundBondItem()
            fundBondItem['fundid'] = fundid
            bond_url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/FundHoldBond.aspx?PostId=" + fundid
            yield scrapy.Request(url=bond_url, meta={'fundBondItem': fundBondItem}, callback=self.bond_parse,
                                 dont_filter=True)


            # 爬取公司信息
            cookies = "icbcUserAnalysisId=2019040912777339; filtervertion=D3F6C6AF-4D7E-403e-8D5A-9CCFC452F040; ismobile=false; ASP.NET_SessionId=4um1gnbgru03tcv3rxlhsmue"
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflat',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Cookie': cookies,
                'Host': 'www.icbc.com.cn',
                'Pragma': 'no-cache',
                'Referer': 'http://www.icbc.com.cn/icbc/%E7%BD%91%E4%B8%8A%E5%9F%BA%E9%87%91/%E5%9F%BA%E9%87%91%E5%B9%B3%E5%8F%B0/%E5%85%AC%E5%8F%B8%E6%A6%82%E5%86%B5.htm?PostId='+fundid,
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            }
            company_url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/FundCompany.aspx?PostId=" + fundid
            yield scrapy.Request(url=company_url, headers=headers, callback=self.company_parse, dont_filter=True)



    # 爬取每个基金的基本信息1
    def detail_parse(self, response):
        fundInfoItem = response.meta['fundInfoItem']
        fundInfoItem['fundtype'] = response.xpath('//*[@id="fundTd27"]/text()').extract_first()
        if fundInfoItem['fundtype']=="" or fundInfoItem['fundtype']==None:
            fundInfoItem['fundtype'] = response.xpath('//*[@id="fundTd3"]/text()').extract_first()
        fundInfoItem['currtype'] = response.xpath('//*[@id="fundTd29"]/text()').extract_first()
        fundInfoItem['lbbaseqg'] = response.xpath('//*[@id="fundTd12"]/text()').extract_first()
        # 爬取基本信息2+基金经理信息
        detail2_url = "http://www.icbc.com.cn/ICBCDynamicSite/site/Fund/FundGeneral.aspx?PostId=" + fundInfoItem[
            'fundid']
        yield scrapy.Request(url=detail2_url, meta={'fundInfoItem': fundInfoItem}, callback=self.detail2_parse,
                             dont_filter=True)

    # 爬取基本信息2+基金经理信息
    def detail2_parse(self, response):
        fundInfoItem = response.meta['fundInfoItem']
        fundid = fundInfoItem['fundid']
        # fundinfo：基金概况信息
        fundInfoItem['shortname'] = response.xpath('//*[@id="lbFundShortName"]/text()').extract_first()
        fundInfoItem['fundcompanyname'] = response.xpath('//*[@id="lbFundCOMPANYID"]/text()').extract_first()
        fundInfoItem['lbbasechg'] = response.xpath('//*[@id="lbFundGuiMo"]/text()').extract_first()
        fundInfoItem['lbbasecreate'] = response.xpath('//*[@id="lbFundCREATED_DATE"]/text()').extract_first()
        # fundInfoItem['managers'] = response.xpath('//*[@id="lbFundMan"]/text()').extract_first()
        managerList = response.xpath('//*[@id="lbManager"]/table')
        # if len(managerList) == 0:
        #     fundInfoItem['managers'] = None
        yield fundInfoItem

        for manager in managerList:
            # 基金经理信息
            fundManagerItem = FundManagerItem()
            fundManagerItem['itemtype'] = "fundManagerItem"
            # 经理姓名
            managername = manager.xpath('tr[1]/td[2]/text()').extract_first()
            managernamenew = ''.join(managername.split())
            fundManagerItem['managername'] = managernamenew
            # 履历
            fundManagerItem['resume'] = manager.xpath('tr[2]/td[2]/text()').extract_first()
            # 获奖情况
            fundManagerItem['awards'] = manager.xpath('tr[4]/td[2]/text()').extract_first()
            # 基金公司
            fundManagerItem['fundcompany'] = manager.xpath('//*[@id="lbFundCOMPANYID"]/text()').extract_first()
            # 年限
            fundManagerItem['years'] = manager.xpath('tr[7]/td[2]/text()').extract_first()

            yield fundManagerItem

            # 基金经理现任基金
            currFundRelItem = CurrFundRelItem()
            currFundRelItem['itemtype'] = "currFundRelItem"
            # 基金ID
            currFundRelItem['fundid'] = fundid
            # 经理ID
            currFundRelItem['managername'] = managernamenew
            # 基金公司
            currFundRelItem['fundcompany'] = manager.xpath('//*[@id="lbFundCOMPANYID"]/text()').extract_first()
            # 年限
            currFundRelItem['years'] = manager.xpath('tr[7]/td[2]/text()').extract_first()

            yield currFundRelItem

            # 基金经理历任基金
            servedFundItemList = manager.xpath('tr[3]/td[2]/a')
            for servedFundItem in servedFundItemList:
                fundItem = servedFundItem.xpath('@onclick').extract_first()
                fundid = ''.join([x for x in fundItem if x.isdigit()])
                servedFundRelItem = ServedFundRelItem()
                servedFundRelItem['itemtype'] = "servedFundRelItem"
                # 历任基金ID
                servedFundRelItem['fundid'] = str(fundid)
                # 经理ID
                servedFundRelItem['managername'] = managernamenew
                # 基金公司
                servedFundRelItem['fundcompany'] = manager.xpath('//*[@id="lbFundCOMPANYID"]/text()').extract_first()
                # 年限
                servedFundRelItem['years'] = manager.xpath('tr[7]/td[2]/text()').extract_first()

                yield servedFundRelItem




    # 爬取基金净值数据
    def pefor_parse(self, response):
        fundPerformanceItem = response.meta['fundPerformanceItem']
        fundPerformanceItem['itemtype'] = "fundperformanceitem"
        # 一周回报率
        fundPerformanceItem['return_1week'] = response.xpath('//*[@id="lbWeek"]/text()').extract_first()
        # 一月回报率
        fundPerformanceItem['return_1month'] = response.xpath('//*[@id="lbMonth"]/text()').extract_first()
        # 三月回报率
        fundPerformanceItem['return_3month'] = response.xpath('//*[@id="lbThreeM"]/text()').extract_first()
        # 六月回报率
        fundPerformanceItem['return_6month'] = response.xpath('//*[@id="lbSixM"]/text()').extract_first()
        # 一年回报率
        fundPerformanceItem['return_1year'] = response.xpath('//*[@id="lbYear"]/text()').extract_first()
        # 今年回报率
        fundPerformanceItem['return_thisyear'] = response.xpath('//*[@id="lbTwoYear"]/text()').extract_first()
        # 两年回报率
        fundPerformanceItem['return_2year'] = response.xpath('//*[@id="lbToYear"]/text()').extract_first()
        # 成立以来回报率
        fundPerformanceItem['return_base'] = response.xpath('//*[@id="lbCreate"]/text()').extract_first()

        yield fundPerformanceItem

    # 爬取资产配置信息
    def asset_parse(self, response):

        itemList = response.xpath('//*[@id="GridViewASSET"]/tr')
        if (len(itemList) > 1):
            del itemList[0]

        for item in itemList:

            fundAssetItem = response.meta['fundAssetItem']

            fundAssetItem['itemtype'] = 'fundAssetItem'
            # 项目
            fundAssetItem['assetitem'] = item.xpath('td[1]/text()').extract_first()
            # 金额（元）
            fundAssetItem['assetamount'] = item.xpath('td[2]/text()').extract_first()
            # 占净值比重%
            fundAssetItem['assetweight'] = item.xpath('td[3]/text()').extract_first()

            yield fundAssetItem

    # 爬取行业投资信息
    def invest_parse(self, response):

        itemList = response.xpath('//*[@id="gvFund"]/tr')
        if (len(itemList) > 1):
            del itemList[0]
        fundAInvestItem = response.meta['fundAInvestItem']
        fundid = fundAInvestItem['fundid']
        for item in itemList:

            fundAInvestItem = FundAInvestItem()

            fundAInvestItem['fundid'] = fundid

            fundAInvestItem['itemtype'] = "fundAInvestItem"
            # 行业简称
            investname = item.xpath('td[2]/text()').extract_first()
            fundAInvestItem['investname'] = ''.join(investname.split())
            # 行业市值
            fundAInvestItem['investamount'] = item.xpath('td[3]/text()').extract_first()
            # 行业市值所占比例
            fundAInvestItem['investweight'] = item.xpath('td[4]/text()').extract_first()

            yield fundAInvestItem

    # 基金持股明细
    def stock_parse(self, response):
        fundStockItem = response.meta['fundStockItem']
        fundid = fundStockItem['fundid']
        itemList = response.xpath('//*[@id="GridViewStock"]/tr')
        if (len(itemList) > 1):
            del itemList[0]
        for item in itemList:
            fundStockItem = FundStockItem()
            fundStockItem['fundid'] = fundid
            fundStockItem['itemtype'] = "fundStockItem"
            # 股票代码
            fundStockItem['stockcode'] = item.xpath('td[2]/span/text()').extract_first()
            # 股票简称
            fundStockItem['stockname'] = item.xpath('td[3]/span/text()').extract_first()
            # 持有股数
            fundStockItem['stockcount'] = item.xpath('td[4]/span/text()').extract_first()
            # 持有市值
            fundStockItem['stockamount'] = item.xpath('td[5]/span/text()').extract_first()
            # 持有市值比例
            fundStockItem['stockweight'] = item.xpath('td[6]/span/text()').extract_first()
            yield fundStockItem

    # 基金持债明细
    def bond_parse(self, response):
        fundBondItem = response.meta['fundBondItem']
        fundid = fundBondItem['fundid']
        itemList = response.xpath('//*[@id="GridView1"]/tr')
        if (len(itemList) > 1):
            del itemList[0]
        for item in itemList:
            fundBondItem = FundBondItem()
            fundBondItem['fundid'] = fundid
            fundBondItem['itemtype'] = "fundBondItem"
            # 债券代码
            fundBondItem['bondcode'] = item.xpath('td[2]/span/text()').extract_first()
            # 债券简称
            fundBondItem['bondname'] = item.xpath('td[3]/span/text()').extract_first()
            # 持有市值
            fundBondItem['bondamount'] = item.xpath('td[4]/span/text()').extract_first()
            # 持有市值比例
            fundBondItem['bondweight'] = item.xpath('td[5]/span/text()').extract_first()
            yield fundBondItem

    # 爬取公司信息
    def company_parse(self, response):

        fundCompanyItem = FundCompanyItem()

        fundCompanyItem['itemtype'] = 'fundCompanyItem'
        # 基金公司名称
        fundCompanyItem['companyname'] = response.xpath('//*[@id="lbFundComName"]/text()').extract_first()
        # 简称
        fundCompanyItem['shortname'] = response.xpath('//*[@id="lbFundComShort"]/text()').extract_first()
        # 注册资本
        fundCompanyItem['registmoney'] = response.xpath('//*[@id="lbREGIST_MONEY"]/text()').extract_first()
        # 是否上市
        fundCompanyItem['is_onmarket'] = response.xpath('//*[@id="lbIS_ONMARKET"]/text()').extract_first()
        # 办公地址
        fundCompanyItem['address'] = response.xpath('//*[@id="lbADDRESS"]/text()').extract_first()
        # 客服电话
        fundCompanyItem['servicetel'] = response.xpath('//*[@id="lbCUSTOMER_SERVICE_TEL"]/text()').extract_first()
        # 公司网址
        fundCompanyItem['website'] = response.xpath('//*[@id="lbWEB0"]/text()').extract_first()
        # 电子邮箱
        fundCompanyItem['email'] = response.xpath('//*[@id="lbEMAIL"]/text()').extract_first()
        # 传真
        fundCompanyItem['fax'] = response.xpath('//*[@id="lbFAX"]/text()').extract_first()

        yield fundCompanyItem





