import datetime

import scrapy

from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from Icbc.mpsitems import AccountGold, AgencyGoldDefer, AgencyGoldActual


class GoldCrawlSpider(scrapy.Spider):
    name = 'goldCrawl'
    allowed_domains = ['mybank.icbc.com.cn']
    # start_urls = ["https://mybank.icbc.com.cn/icbc/newperbank/perbank3/gold/frame_acgold_index_out.jsp?Area_code=0200&requestChannel=302"]
    menuFlag = 0
    start_urls = ["http://www.icbc.com.cn/ICBCDynamicSite/Charts/GoldTendencyPicture.aspx"]


    def __init__(self):
        super(GoldCrawlSpider, self).__init__(name='goldCrawl')
        option = FirefoxOptions()
        option.headless = True
        self.driver = webdriver.Firefox(options=option,executable_path='/usr/local/bin/geckodriver/geckodriver')

    # 爬取每页的基金列表数据
    def parse(self, response):
            itemList = response.xpath('//*[@id="TABLE2"]/tbody/tr')
            # 爬取基金净值信息
            accountGold_url = "http://www.icbc.com.cn/ICBCDynamicSite/Charts/GoldTendencyPicture.aspx"
            yield scrapy.Request(url=accountGold_url, callback=self.accountGold_parse, dont_filter=True)



    # 账户贵金属信息
    def accountGold_parse(self, response):
        itemList = response.xpath('//*[@id="TABLE1"]/tbody/tr')
        if (len(itemList) > 1):
            del itemList[0]
            # print(itemList)
            updateTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for item in itemList:
            accountGold = AccountGold()
            accountGold['item_mark'] = "accountGold"
            # 品种
            ac1=item.xpath('td[1]/text()').extract_first().strip()
            accountGold['item_type'] = ac1.strip()
            # 涨跌 0为上涨 1为下跌 2为持平
            ac2=item.xpath('td[2]/img/@src').extract_first()
            if "0.gif" in ac2:
                mc=0
            elif "1.gif" in ac2:
                mc=1
            elif "2.gif" in ac2:
                mc=2
            # 银行买入价
            accountGold['risefall'] = mc
            ac3=item.xpath('td[3]/text()').extract_first()
            accountGold['bank_buying_price'] = ac3.strip()
            # 银行卖出价
            ac4=item.xpath('td[4]/text()').extract_first()
            accountGold['bank_selling_price'] = ac4.strip()
            # 中间价
            ac5=item.xpath('td[5]/text()').extract_first()
            accountGold['middle_price'] = ac5.strip()
            # 当日涨跌值
            ac6=item.xpath('td[6]/text()').extract_first()
            accountGold['day_risefall_value'] = ac6.strip()
            # 当日涨跌幅
            ac7=item.xpath('td[7]/text()').extract_first()
            accountGold['day_risefall_range'] = ac7.strip()
            # 更新时间
            ac8=item.xpath('td[8]/text()').extract_first()
            accountGold['year_risefall_range'] = ac8.strip()
            accountGold['update_time'] = updateTime
            print(accountGold)
            yield accountGold
        #代理贵金属递延
        itemList = response.xpath('//*[@id="TABLE2"]/tbody/tr')
        if (len(itemList) > 1):
            del itemList[0]
        for item in itemList:
            agencyGoldDefer = AgencyGoldDefer()
            agencyGoldDefer['item_mark'] = "agencyGoldDefer"
            # 品种
            ag1=item.xpath('td[1]/text()').extract_first()
            agencyGoldDefer['item_type'] = ag1.strip()
            # 当前价
            ag2=item.xpath('td[2]/text()').extract_first()
            agencyGoldDefer['currency_price'] = ag2.strip()
            # 涨跌
            ag3=item.xpath('td[3]/img/@src').extract_first()
            if "0.gif" in ag3:
                mg=0
            elif "1.gif" in ag3:
                mg=1
            elif "2.gif" in ag3:
                mg=2
            agencyGoldDefer['currency_risefall'] = mg
            # 涨跌幅
            ag4=item.xpath('td[4]/text()').extract_first()
            agencyGoldDefer['risefall_range'] = ag4.strip()
            # 成交量（手）
            ag5=item.xpath('td[5]/text()').extract_first()
            agencyGoldDefer['turnover'] = ag5.strip()
            # 开盘价
            ag6=item.xpath('td[6]/text()').extract_first()
            agencyGoldDefer['opening_price'] = ag6.strip()
            # 昨收价
            ag7=item.xpath('td[7]/text()').extract_first()
            agencyGoldDefer['closing_price'] = ag7.strip()
            # 最高价
            ag8=item.xpath('td[8]/text()').extract_first()
            agencyGoldDefer['highest_price'] = ag8.strip()
            # 最低价
            ag9=item.xpath('td[9]/text()').extract_first()
            agencyGoldDefer['lowest_price'] = ag9.strip()
            # 更新时间
            ag10=item.xpath('td[10]/text()').extract_first()
            agencyGoldDefer['update_time'] = ag10.strip()
            print(agencyGoldDefer)
            yield agencyGoldDefer
        #代理贵金属现货
        itemList = response.xpath('//*[@id="TABLE3"]/tbody/tr')
        if (len(itemList) > 1):
            del itemList[0]
        for item in itemList:
            agencyGoldActual = AgencyGoldActual()
            agencyGoldActual['item_mark'] = "agencyGoldActual"
            # 品种
            age1=item.xpath('td[1]/text()').extract_first()
            agencyGoldActual['item_type'] = age1.strip()
            # 当前价
            age2=item.xpath('td[2]/text()').extract_first()
            agencyGoldActual['currency_price'] = age2.strip()
            # 涨跌
            age3=item.xpath('td[3]/img/@src').extract_first()
            if "0.gif" in age3:
                mge=0
            elif "1.gif" in age3:
                mge=1
            elif "2.gif" in age3:
                mge=2
            agencyGoldActual['currency_risefall'] = mge
            # 涨跌幅
            age4=item.xpath('td[4]/text()').extract_first()
            agencyGoldActual['risefall_range'] = age4.strip()
            # 成交量（手）
            age5=item.xpath('td[5]/text()').extract_first()
            agencyGoldActual['turnover'] = age5.strip()
            # 开盘价
            age6=item.xpath('td[6]/text()').extract_first()
            agencyGoldActual['opening_price'] = age6.strip()
            # 昨收价
            age7=item.xpath('td[7]/text()').extract_first()
            agencyGoldActual['closing_price'] = age7.strip()
            # 最高价
            age8=item.xpath('td[8]/text()').extract_first()
            agencyGoldActual['highest_price'] = age8.strip()
            # 最低价
            age9=item.xpath('td[9]/text()').extract_first()
            agencyGoldActual['lowest_price'] = age9.strip()
            # 更新时间
            age10=item.xpath('td[10]/text()').extract_first()
            agencyGoldActual['update_time'] = age10.strip()
            print(agencyGoldActual)
            yield agencyGoldActual





