import os
from enum import Enum

import sqlalchemy as db


class DBTable(Enum):
    """
    Class for all the tables
    """
    Order = "Order"
    OrderLine = "OrderLine"
    Product = "Product"
    ProductPromotion = "ProductPromotion"
    Promotion = "Promotion"
    VendorCommission = "VendorCommissions"


def create_engine():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    if os.getenv('DEPLOYMENT_PROJECT') == 'local':
        if not db_user:
            raise ValueError("DB_USER environment variable not set")
        if not db_password:
            raise ValueError("DB_PASSWORD environment variable not set")
        if not db_host:
            raise ValueError("DB_HOST environment variable not set")
        if not db_port:
            raise ValueError("DB_PORT environment variable not set")
        if not db_name:
            raise ValueError("DB_NAME environment variable not set")
    else:
        # TODO prod
        pass

    connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return db.create_engine(connection_string)
