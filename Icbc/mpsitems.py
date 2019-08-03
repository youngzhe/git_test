# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#http://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx
# 外汇牌价表
class ExchangeRate(scrapy.Item):
    item_mark = scrapy.Field()
    # 币种
    currency_type = scrapy.Field()
    # 现汇买入价
    currency_buying_price = scrapy.Field()
    # 现钞买入价
    cash_buying_price = scrapy.Field()
    # 现汇卖出价
    currency_selling_price = scrapy.Field()
    # 现钞卖出价
    cash_selling_price = scrapy.Field()
    # 发布时间
    update_time = scrapy.Field()
    # 单位：人民币/100外币
    unit = scrapy.Field()

#https://mybank.icbc.com.cn/icbc/newperbank/perbank3/gold/frame_acgold_index_out.jsp?Area_code=0200&requestChannel=302
# 账户贵金属
class AccountGold(scrapy.Item):
    item_mark = scrapy.Field()
    # 品种
    item_type = scrapy.Field()
    # 涨跌
    risefall = scrapy.Field()
    # 银行买入价
    bank_buying_price = scrapy.Field()
    # 银行卖出价
    bank_selling_price = scrapy.Field()
    # 中间价
    middle_price = scrapy.Field()
    # 当日涨跌值
    day_risefall_value = scrapy.Field()
    # 当日涨跌幅
    day_risefall_range = scrapy.Field()
    # 当年涨跌幅
    year_risefall_range = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()


# 账户贵金属指数
class AccountGold_index(scrapy.Item):
    item_mark = scrapy.Field()
    # 品种
    item_type = scrapy.Field()
    # 涨跌
    risefall = scrapy.Field()
    # 银行买入价
    bank_buying_price = scrapy.Field()
    # 银行卖出价
    bank_selling_price = scrapy.Field()
    # 中间价
    middle_price = scrapy.Field()
    # 当日涨跌值
    day_risefall_value = scrapy.Field()
    # 当日涨跌幅
    day_risefall_range = scrapy.Field()
    # 当年涨跌幅
    year_risefall_range = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()

# 积存贵金属
class StoreGold(scrapy.Item):
    item_mark = scrapy.Field()
    # 金种
    item_type = scrapy.Field()
    # 实时主动 积存价格
    real_active_store_price = scrapy.Field()
    # 涨跌
    real_active_store_risefall = scrapy.Field()
    # 最低价
    lowest_price = scrapy.Field()
    # 最高价
    highest_price = scrapy.Field()
    # 定期积存价
    regular_store_price = scrapy.Field()
    # 涨跌
    store_risefall = scrapy.Field()
    # 赎回价
    redeem_price = scrapy.Field()
    # 涨跌
    redeem_risefall = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()

# 代理贵金属递延
class AgencyGoldDefer(scrapy.Item):
    item_mark = scrapy.Field()
    # 品种
    item_type = scrapy.Field()
    # 当前价
    currency_price = scrapy.Field()
    # 涨跌
    currency_risefall = scrapy.Field()
    # 涨跌幅
    risefall_range = scrapy.Field()
    # 成交量（手）
    turnover = scrapy.Field()
    # 开盘价
    opening_price = scrapy.Field()
    # 昨收价
    closing_price = scrapy.Field()
    # 最高价
    highest_price = scrapy.Field()
    # 最低价
    lowest_price = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()



# 代理贵金属现货
class AgencyGoldActual(scrapy.Item):
    item_mark = scrapy.Field()
    #品种
    item_type = scrapy.Field()
    # 当前价
    currency_price = scrapy.Field()
    # 涨跌
    currency_risefall = scrapy.Field()
    # 涨跌幅
    risefall_range = scrapy.Field()
    # 成交量（手）
    turnover = scrapy.Field()
    #开盘价
    opening_price = scrapy.Field()
    # 昨收价
    closing_price = scrapy.Field()
    # 最高价
    highest_price = scrapy.Field()
    # 最低价
    lowest_price = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()

#https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&Area_code=0200&requestChannel=302
# 明星理财产品
class StarFinance(scrapy.Item):
    item_mark = scrapy.Field()
    # 名称
    product_name = scrapy.Field()
    # 预期年化收益率
    performance_banchmark = scrapy.Field()
    # 起购金额
    up_purchase_amount = scrapy.Field()
    # 期限
    invesment_period = scrapy.Field()
    # 风险等级
    risk_class = scrapy.Field()
    # 最近购买开放日
    raising_period = scrapy.Field()
    # 更新日期
    update_time = scrapy.Field()

#https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&menuLabel=10$17$TJ&Area_code=0200&requestChannel=302
# 私行推荐产品理财 nowPageNum_turn=1
class PrivateRecommendFinance(scrapy.Item):
    item_mark = scrapy.Field()
    # 名称
    product_name = scrapy.Field()
    # 预期年化收益率
    performance_banchmark = scrapy.Field()
    # 起购金额
    up_purchase_amount = scrapy.Field()
    # 期限
    invesment_period = scrapy.Field()
    # 风险等级
    risk_class = scrapy.Field()
    # 最近购买开放日
    raising_period = scrapy.Field()
    # 更新日期
    update_time = scrapy.Field()

#私行推荐基金
#https://mybank.icbc.com.cn/icbc/newperbank/perbank3/fund/frame_fund_nologin.jsp?Flag=1&pageFlag=0&menuFlag=9&Area_code=&requestChannel=302&currPageNum=4
class PrivateRecommendFund(scrapy.Item):
    item_mark = scrapy.Field()
    # 代码
    item_code = scrapy.Field()
    # 名称
    item_name = scrapy.Field()
    # 单位净值/上一日万分收益
    unit_net_value = scrapy.Field()
    # 累计净值/七日年化收益率
    total_net_value = scrapy.Field()
    # 日涨幅
    day_risefall = scrapy.Field()
    # 近三个月涨幅
    month_risefall = scrapy.Field()
    # 晨星评级
    grade = scrapy.Field()
    # 产品状态
    status = scrapy.Field()
    # 更新日期
    update_time = scrapy.Field()

#