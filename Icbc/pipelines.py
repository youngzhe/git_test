# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# import sys
# import MySQLdb
#
default_encoding = 'utf-8'
#
# if sys.getdefaultencoding() != default_encoding:
#     reload(sys)
#     sys.setdefaultencoding(default_encoding)




class FundPipeline(object):

    def __init__(self):
        #连接数据库
        self.connect = pymysql.connect(host='localhost', user='root', password='123456', db='spider', port=3306)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        if (item['item_mark'] == "exchangeRate"):
            self.cursor.execute(
                "INSERT INTO apps_exchange_rate (currency_type, currency_buying_price, cash_buying_price, currency_selling_price,"
                "cash_selling_price, update_time, unit) "
                "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                (item['currency_type'], item['currency_buying_price'], item['cash_buying_price'],
                 item['currency_selling_price'], item['cash_selling_price'], item['update_time'],
                 item['unit']))

        # 2、基金净值
        if (item['item_mark'] == "accountGold"):
            self.cursor.execute(
                "INSERT INTO apps_account_gold (item_type, risefall, bank_buying_price, bank_selling_price,"
                "middle_price, day_risefall_value, day_risefall_range, year_risefall_range, update_time) "
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (item['item_type'], item['risefall'], item['bank_buying_price'],
                 item['bank_selling_price'], item['middle_price'], item['day_risefall_value'],
                 item['day_risefall_range'], item['year_risefall_range'], item['update_time']))

        if (item['item_mark'] == "agencyGoldActual"):
            self.cursor.execute(
                "INSERT INTO apps_agency_gold_actual (item_type, currency_price, currency_risefall, risefall_range,"
                "turnover, opening_price, closing_price, highest_price, lowest_price,update_time) "
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (item['item_type'], item['currency_price'], item['currency_risefall'],
                 item['risefall_range'], item['turnover'], item['opening_price'],
                 item['closing_price'], item['highest_price'], item['lowest_price'], item['update_time']))

        if (item['item_mark'] == "agencyGoldDefer"):
            self.cursor.execute(
                "INSERT INTO apps_agency_gold_defer (item_type, currency_price, currency_risefall, risefall_range,"
                "turnover, opening_price, closing_price, highest_price, lowest_price,update_time) "
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (item['item_type'], item['currency_price'], item['currency_risefall'],
                 item['risefall_range'], item['turnover'], item['opening_price'],
                 item['closing_price'], item['highest_price'], item['lowest_price'], item['update_time']))

        if (item['item_mark'] == "starFinance"):
            self.cursor.execute(
                "INSERT INTO apps_star_finance (product_name, performance_banchmark, up_purchase_amount, invesment_period,"
                "risk_class, raising_period, update_time) "
                "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                (item['product_name'], item['performance_banchmark'], item['up_purchase_amount'],
                 item['invesment_period'], item['risk_class'], item['raising_period'], item['update_time']))

        if (item['item_mark'] == "privateRecommendFinance"):
            self.cursor.execute(
                "INSERT INTO apps_private_recommend (product_name, performance_banchmark, up_purchase_amount, investment_period,"
                "risk_class, raising_period, update_time) "
                "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                (item['product_name'], item['performance_banchmark'], item['up_purchase_amount'],
                 item['investment_period'], item['risk_class'], item['raising_period'], item['update_time']))

        if (item['item_mark'] == "privateRecommendFund"):
            self.cursor.execute(
                "INSERT INTO apps_private_recommend_fund (item_code, item_name, unit_net_value, total_net_value,"
                "day_risefall, month_risefall,grade,status, update_time) "
                "VALUES(%s, %s, %s, %s, %s, %s, %s,%s, %s)",
                (item['item_code'], item['item_name'], item['unit_net_value'],
                 item['total_net_value'], item['day_risefall'], item['month_risefall'],item['grade'],item['status'], item['update_time']))


        self.connect.commit()
        return item

