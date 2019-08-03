# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 基金信息
class FundInfoItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 列表列数
    itemcount = scrapy.Field()
    # 基金代码
    fundid = scrapy.Field()
    # 基金名称
    fundname = scrapy.Field()
    # 基金类型：公募、非公募
    ftype = scrapy.Field()
    # 币种
    currtype = scrapy.Field()
    # 基金产品类型：股票型等等
    fundtype = scrapy.Field()
    # 基金规模
    lbbasechg = scrapy.Field()
    # 成立日期
    lbbasecreate = scrapy.Field()
    # 起购金额
    lbbaseqg = scrapy.Field()
    #基金简称
    shortname = scrapy.Field()
    # 基金公司名称
    fundcompanyname = scrapy.Field()
    # 基金经理
    managers = scrapy.Field()

# 基金当前净值
class FundPerformanceItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 单位净值
    buyprice = scrapy.Field()
    # 累计净值
    sumprice = scrapy.Field()
    # 日涨跌
    fi_nav3 = scrapy.Field()
    # 一周回报率
    return_1week = scrapy.Field()
    # 一月回报率
    return_1month = scrapy.Field()
    # 三月回报率
    return_3month = scrapy.Field()
    # 六月回报率
    return_6month = scrapy.Field()
    # 一年回报率
    return_1year = scrapy.Field()
    # 今年回报率
    return_thisyear = scrapy.Field()
    # 两年回报率
    return_2year = scrapy.Field()
    # 成立以来回报率
    return_base = scrapy.Field()
    # 基金ID
    fundid = scrapy.Field()

# 基金费率
class FundRateItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 费率
    frate = scrapy.Field()
    # 费率类型
    ratetype = scrapy.Field()
    # 费率金额
    ratemoney = scrapy.Field()
    # 持有期限
    funddate = scrapy.Field()
    # 基金ID
    fundid = scrapy.Field()

# 基金投资方向
# 1、基金资产配置
class FundAssetItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 项目
    assetitem = scrapy.Field()
    # 金额（元）
    assetamount = scrapy.Field()
    # 占净值比重%
    assetweight = scrapy.Field()
    # 基金ID
    fundid = scrapy.Field()

# 2、基金行业投资
class FundAInvestItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 行业简称
    investname = scrapy.Field()
    # 行业市值
    investamount = scrapy.Field()
    # 行业市值所占比例
    investweight = scrapy.Field()
    # 基金ID
    fundid = scrapy.Field()

# 3、基金持股明细
class FundStockItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 股票代码
    stockcode = scrapy.Field()
    # 股票简称
    stockname = scrapy.Field()
    # 持有股数
    stockcount = scrapy.Field()
    # 持有市值
    stockamount = scrapy.Field()
    # 持有市值比例
    stockweight = scrapy.Field()
    # 基金ID
    fundid = scrapy.Field()

# 4、基金持债明细
class FundBondItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 债券代码
    bondcode = scrapy.Field()
    # 债券简称
    bondname = scrapy.Field()
    # 持有市值
    bondamount = scrapy.Field()
    # 持有市值比例
    bondweight = scrapy.Field()
    # 基金ID
    fundid = scrapy.Field()

# 基金公司名称
class FundCompanyItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 基金公司名称
    companyname = scrapy.Field()
    # 简称
    shortname = scrapy.Field()
    # 注册资本
    registmoney = scrapy.Field()
    # 是否上市
    is_onmarket = scrapy.Field()
    # 办公地址
    address = scrapy.Field()
    # 客服电话
    servicetel = scrapy.Field()
    # 公司网址
    website = scrapy.Field()
    # 电子邮箱
    email = scrapy.Field()
    # 传真
    fax = scrapy.Field()

# 基金经理
class FundManagerItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 经理姓名
    managername = scrapy.Field()
    # 履历
    resume = scrapy.Field()
    # 获奖情况
    awards = scrapy.Field()
    # 基金公司
    fundcompany = scrapy.Field()
    # 年限
    years = scrapy.Field()

# 基金经理和现任基金中间关系
class CurrFundRelItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 基金ID
    fundid = scrapy.Field()
    # 经理ID
    managername = scrapy.Field()
    # 基金公司
    fundcompany = scrapy.Field()
    # 年限
    years = scrapy.Field()

# 基金经理和历任基金中间关系
class ServedFundRelItem(scrapy.Item):
    itemtype = scrapy.Field()
    # 基金ID
    fundid = scrapy.Field()
    # 经理ID
    managername = scrapy.Field()
    # 基金公司
    fundcompany = scrapy.Field()
    # 年限
    years = scrapy.Field()


