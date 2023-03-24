import logging

import sqlalchemy as db
from flask import abort
from sqlalchemy.exc import OperationalError

from db.db import create_engine
from db.queries import QUERY_GET_TOTAL_NUMBER_OF_ITEMS_SOLD_PER_DAY, QUERY_GET_TOTAL_ORDERS_PER_CUSOTOMER_DAILY, \
    QUERY_GET_TOTAL_DISCOUNT_GIVEN_PER_DAY, QUERY_GET_AVERAGE_DISCOUNTRATE_ON_ITEM_SOLD_PER_DAY, \
    QUERY_GET_TOTAL_AMOUNT_OF_COMMISSIONS_GENERATED_PER_DAY, \
    QUERY_GET_COMMISION_PER_CATEGORY, QUERY_AVERAGE_ORDER_TOTAL_PER_DAY


def execute_query(query, params):
    try:
        with create_engine().connect() as con:
            result = con.execute(db.text(query).bindparams(
                db.bindparam('date'),
                date=params['date']
            ))
            result_data = result.fetchall()
            if result_data:
                return result_data
            return
    except OperationalError:
        logging.critical("cannot connect to DB")
        abort(502, "cannot connect to DB")


class DailyDbReport:
    @staticmethod
    def total_number_of_items_sold_per_day(date):
        return execute_query(QUERY_GET_TOTAL_NUMBER_OF_ITEMS_SOLD_PER_DAY, {'date': date})

    @staticmethod
    def total_number_of_customers_per_day(date):
        return execute_query(QUERY_GET_TOTAL_ORDERS_PER_CUSOTOMER_DAILY, {'date': date})

    @staticmethod
    def total_discount_per_day(date):
        return execute_query(QUERY_GET_TOTAL_DISCOUNT_GIVEN_PER_DAY, {'date': date})

    @staticmethod
    def AvgDiscountPerItemsPerDay(date):
        return execute_query(QUERY_GET_AVERAGE_DISCOUNTRATE_ON_ITEM_SOLD_PER_DAY, {'date': date})

    @staticmethod
    def AvgPerItemsPerDay(date):
        return execute_query(QUERY_AVERAGE_ORDER_TOTAL_PER_DAY, {'date': date})

    @staticmethod
    def TotalCommissionPerDay(date):
        return execute_query(QUERY_GET_TOTAL_AMOUNT_OF_COMMISSIONS_GENERATED_PER_DAY, {'date': date})

    @staticmethod
    def TotalAvgCommissionPerDay(date):
        return execute_query(QUERY_GET_TOTAL_AMOUNT_OF_COMMISSIONS_GENERATED_PER_DAY, {'date': date})

    @staticmethod
    def GetCommisionPerEachPromotion(date):
        return execute_query(QUERY_GET_COMMISION_PER_CATEGORY, {'date': date})
