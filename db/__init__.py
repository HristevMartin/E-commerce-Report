import logging
import os

import pandas as pd
import sqlalchemy as alchemydb

from db.db import create_engine, DBTable
from db.queries import QUERY_CREATE_ORDER_TABLE, QUERY_CREATE_ORDERLINE_TABLE, QUERY_CREATE_PRODUCT_TABLE, \
    QUERY_CREATE_PROMOTION_TABLE, QUERY_CREATE_PRODUCT_PROMOTION_TABLE, QUERY_CREATE_VendorCommision_TABLE

available_tables = [
    {
        "name": DBTable.Order,
        "query": QUERY_CREATE_ORDER_TABLE,
        "init_fun": None,
        "dumps_path": "orders.csv"
    },
    {
        "name": DBTable.Product,
        "query": QUERY_CREATE_PRODUCT_TABLE,
        "init_fun": None,
        "dumps_path": "products.csv"
    },
    {
        "name": DBTable.OrderLine,
        "query": QUERY_CREATE_ORDERLINE_TABLE,
        "init_fun": None,
        "dumps_path": "order_lines.csv"
    },
    {
        "name": DBTable.Promotion,
        "query": QUERY_CREATE_PROMOTION_TABLE,
        "init_fun": None,
        "dumps_path": "promotions.csv"
    },
    {
        "name": DBTable.ProductPromotion,
        "query": QUERY_CREATE_PRODUCT_PROMOTION_TABLE,
        "init_fun": None,
        "dumps_path": "product_promotions.csv"
    },
    {
        "name": DBTable.VendorCommission,
        "query": QUERY_CREATE_VendorCommision_TABLE,
        "init_fun": None,
        "dumps_path": "commissions.csv"
    }
]


def create_table(QUERIES: str, table_name: DBTable) -> bool:
    created = False
    with create_engine().connect() as con:
        with con.begin():
            try:
                if not con.dialect.has_table(con, table_name.value):
                    for QUERY in QUERIES.split(";"):
                        if QUERY and QUERY != '\n':
                            con.execute(alchemydb.text(QUERY))
                    created = True
            except Exception as ex:
                print(ex)
    return created


def insert_local_dumps(table_name, dumps_path, chunk_size=5000):
    engine = create_engine()
    df = pd.read_csv(dumps_path)
    try:
        df.to_sql(name=table_name, con=engine, if_exists="append", index=False)
    except Exception as ex:
        logging.info('Exception while inserting the data in the database', ex)
    return True


def create_tables():
    for table in available_tables:

        failed = False
        created = False

        logging.info(f"INIT DB TABLE:")
        try:
            created = create_table(table["query"], table["name"])
        except:
            failed = True
            logging.exception(f"failed to INIT the TABLE ")

        if created:
            if os.environ.get('DUMPS_PATH'):
                inserted = insert_local_dumps(table['name'].value,
                                              os.path.join(os.environ.get('DUMPS_PATH'), table["dumps_path"]))
                if inserted:
                    logging.info(f"local dumps inserted into "
                                 f"DB TABLE: {table['name'].value} successfully")
                else:
                    logging.warning(f"Cannot add dumps because DUMPS_PATH env var is missed")
        elif failed:
            logging.info(f"Failed Table: {table['name'].value} while creating")
        elif not failed:
            logging.info(f"DB TABLE: {table['name'].value} is already exists")
