from report.dbParser import DailyDbReport


def get_daily_report(date_str: str) -> dict:
    """
    This function calls the database methods responsible for fetching the data from the database.
    :param date_str:
    :return: Dictionary containing daily report
    """

    total_per_day = int(DailyDbReport.total_number_of_items_sold_per_day(date_str)[0][0])
    total_number_of_customers_per_day = DailyDbReport.total_number_of_customers_per_day(date_str)[0][0]
    total_discount_per_day = DailyDbReport.total_discount_per_day(date_str)[0][0]
    total_avg_discount_sold_items_per_day = DailyDbReport.AvgDiscountPerItemsPerDay(date_str)[0][0]
    total_avg_sold_items_per_day = DailyDbReport.AvgPerItemsPerDay(date_str)[0][0]
    total_commission_per_day = DailyDbReport.TotalCommissionPerDay(date_str)[0][0]
    order_average = DailyDbReport.TotalAvgCommissionPerDay(date_str)[0][0]

    get_commission_per_promotion_all_categories = DailyDbReport.GetCommisionPerEachPromotion(date_str)

    get_commission_per_promotion_all_categories_dict = {k: v for k, v in get_commission_per_promotion_all_categories}

    result = {
        "items": total_per_day,
        "customers": total_number_of_customers_per_day,
        "total_discount_amount": round(total_discount_per_day, 2),
        "discount_rate_avg": total_avg_discount_sold_items_per_day,
        "order_total_avg": round(total_avg_sold_items_per_day, 2),
        "commissions": {
            "promotions": {**get_commission_per_promotion_all_categories_dict},
            "total": round(total_commission_per_day, 2),
            "order_average": round(order_average, 2)
        }
    }

    return result
